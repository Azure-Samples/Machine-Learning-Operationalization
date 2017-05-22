from __future__ import print_function
from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic)
from IPython.utils.ipstruct import Struct
import os
import argparse
import shlex
import re

from cStringIO import StringIO
import sys


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # free up some memory
        sys.stdout = self._stdout


@magics_class
class AMLHelpers(Magics):
    @staticmethod
    def print_and_update_env(k, v):
        os.environ[k] = v
        print(' os.environ["{}"]="{}"'.format(k, v))
        return 'export {}={}'.format(k, v)

    @cell_magic
    def save_file(self, parameter_s='', cell=None):
        opts, arg_str = self.parse_options(parameter_s, 'f:', list_all=True, posix=False)
        if cell is not None:
            arg_str += '\n' + cell

        return self._save_file(arg_str, opts, self.shell.user_ns)

    @line_magic
    def list_subs(self, line):
        from azure.cli.core._profile import Profile
        try:
            from azure.cli.core.util import CLIError
        except ImportError:
            from azure.cli.core._util import CLIError
        self._redirect_logging('az.azure.cli.core._profile')
        profile = Profile()
        try:
            profile.get_subscription()
        except CLIError:
            profile.find_subscriptions_on_login(True, None, None, None, None)
        subs = profile.load_cached_subscriptions()
        if not subs:
            print('No subscriptions available.')
            print('Please run `az login` from the console then try again')
            return
        print("Available subscriptions:\n  {}".format('\n  '.join(
            [sub['name'] for sub in subs])))

    @line_magic
    def select_sub(self, line):
        from azure.cli.core._profile import Profile
        try:
            from azure.cli.core.util import CLIError
        except ImportError:
            from azure.cli.core._util import CLIError
        self._redirect_logging('az.azure.cli.core._profile')
        p = argparse.ArgumentParser()
        p.add_argument('subscription')
        parsed_args = p.parse_args(shlex.split(line))
        profile = Profile()
        subs = profile.load_cached_subscriptions()
        if not subs:
            profile.find_subscriptions_on_login(True, None, None, None, None)

        try:
            profile.set_active_subscription(parsed_args.subscription)
            print('Active subscription set to {}'.format(
                profile.get_subscription()['name']))
        except CLIError as exc:
            print(exc)
            print('Active subscription remains {}'.format(
                profile.get_subscription()['name']))

    @line_magic
    def check_deployment(self, line):
        from azure.cli.core._profile import Profile
        from azure.cli.command_modules.ml.env import env_setup
        from azure.cli.command_modules.ml._util import JupyterContext
        self._redirect_logging('az.azure.cli.core._profile')

        # validate that user has selected a subscription
        profile = Profile()
        subs = profile.load_cached_subscriptions()
        if not subs:
            print('Please run %%select_sub before attempting to query.')
            return

        env_setup(True, None, None, None, None, None, context=JupyterContext())

    @line_magic
    def aml_env_setup(self, line):
        from azure.cli.core._profile import Profile
        self._redirect_logging('az.azure.cli.core._profile')
        p = argparse.ArgumentParser()
        p.add_argument('-n', '--name', help='base name for your environment',
                       required=True)
        p.add_argument('-k', dest='kubernetes',
                       help='Flag to indicate kubernetes environment', required=False,
                       action='store_true')
        p.add_argument('-l', dest='local_only', help='Flag to preclude ACS deployment',
                       required=False, action='store_true')
        p.add_argument('-a', dest='service_principal_app_id',
                       help='AppID of service principal', required=False)
        p.add_argument('-p', dest='service_principal_password',
                       help='Client Secret of service principal', required=False)
        parsed_args = p.parse_args(line.split())
        # validate that user has selected a subscription
        profile = Profile()
        subs = profile.load_cached_subscriptions()
        if not subs:
            print('Please run %select_sub before attempting to set up environment.')
            return
        from azure.cli.command_modules.ml.env import env_setup
        from azure.cli.command_modules.ml._util import JupyterContext
        c = JupyterContext()
        c.set_input_response('Continue with this subscription (Y/n)? ', 'y')
        print(
            'Setting up AML environment. Feel free to continue exploring the rest '
            'of your notebook until this cell updates, though kernel will be busy...')
        with Capturing() as output:
            env_setup(None, parsed_args.name, parsed_args.kubernetes,
                      parsed_args.local_only,
                      parsed_args.service_principal_app_id,
                      parsed_args.service_principal_password,
                      c)
        acs_regex = r"az ml env setup -s (?P<deployment_id>[^']+)"
        env_regex = r'export (?P<k>[^=]+)=(?P<v>.+)'

        for line in output:
            s = re.search(acs_regex, line)
            if s:
                print(
                    'To check the status of the deployment, run line magic %check_deployment -d {}'.format(
                        s.group('deployment_id')))
            else:
                s = re.search(env_regex, line)
                if s:
                    self.print_and_update_env(s.group('k'), s.group('v'))
                else:
                    print(line)

        print('These values have also been added to the current environment.')

    @cell_magic
    def publish_realtime_local(self, parameter_s='', cell=None):
        import tempfile
        import azure.cli.command_modules.ml.service.realtime as r
        import azure.cli.command_modules.ml._util as u
        import azure.cli.command_modules.ml.service._realtimeutilities as rtu

        # reload util to get new environment vars
        self.easy_reload(u)
        p = argparse.ArgumentParser()
        p.add_argument('-s', '--schema', help='local path to schema file')
        p.add_argument('-m', '--model', help='local path to model')
        p.add_argument('-n', '--name', help='name of the webservice', required=True)
        p.add_argument('-d', '--dependency', dest='dependencies',
                       help='arbitrary dependencies', action='append', default=[])
        p.add_argument('-p', '--requirements', dest='requirements',
                       help='A pip requirements.txt file of packages needed by the code file.', required=False)
        p.add_argument('-o', '--overwrite', help='flag to overwrite existing service',
                       action='store_true')
        p.add_argument('-r', '--target-runtime', help='Runtime of the web service. Valid runtimes are {}'.format('|'.join(rtu.RealtimeConstants.supported_runtimes)),
                       default='spark-py')
        p.add_argument('-l', '--app-insights-logging-enabled', dest='app_insights_logging_enabled',
                       action='store_true', help='Flag to enable App insights logging.', required=False)
        p.add_argument('-z', '--num-replicas', dest='num_replicas', type=int,
                      default=1, required=False, help='Number of replicas for a Kubernetes service.')
        args = p.parse_args(parameter_s.split())
        context = u.JupyterContext()
        context.local_mode = True
        context.set_input_response(
            'Delete existing service and create new service (y/N)? ',
            'y' if args.overwrite else 'n')
        _, fp = tempfile.mkstemp()
        with open(fp, 'w') as score_file:
            score_file.write(cell)
        try:
            resp_code = r.realtime_service_create(score_file.name,
                                                  dependencies=args.dependencies,
                                                  requirements=args.requirements,
                                                  schema_file=args.schema,
                                                  service_name=args.name,
                                                  verb=False, custom_ice_url='',
                                                  target_runtime=args.target_runtime,
                                                  app_insights_logging_enabled=args.app_insights_logging_enabled,
                                                  num_replicas=args.num_replicas,
                                                  model=args.model,
                                                  context=context)
            if resp_code == 1:
                print('Use -o flag to magic to overwrite the existing service.')
        finally:
            # cleanup
            os.remove(fp)

    @line_magic
    def list_realtime_local(self, line):
        from azure.cli.command_modules.ml.service.realtime import realtime_service_list
        from azure.cli.command_modules.ml._util import JupyterContext
        c = JupyterContext()
        c.local_mode = True
        realtime_service_list(context=c)

    @line_magic
    def view_realtime_local(self, line):
        import azure.cli.command_modules.ml.service.realtime as r
        import azure.cli.command_modules.ml._util as u

        p = argparse.ArgumentParser()
        p.add_argument('-n', '--name', help='name of the webservice', required=True)
        name = p.parse_args(line.split()).name
        context = u.JupyterContext()
        context.local_mode = True
        r.realtime_service_view(service_name=name, context=context)

    @line_magic
    def run_realtime_local(self, line):
        import azure.cli.command_modules.ml.service.realtime as r

        p = argparse.ArgumentParser()
        p.add_argument('-n', '--name', help='name of the webservice', required=True)
        p.add_argument('-d', '--data', help='data to send', default='')
        parsed_args = p.parse_args(shlex.split(line))
        name = parsed_args.name
        input_data = parsed_args.data
        r.realtime_service_run_local(service_name=name, input_data=input_data,
                                     verbose=False)

    @line_magic
    def delete_realtime_local(self, line):
        import azure.cli.command_modules.ml.service.realtime as r

        p = argparse.ArgumentParser()
        p.add_argument('-n', '--name', help='name of the webservice', required=True)
        name = p.parse_args(line.split()).name
        r.realtime_service_delete_local(service_name=name, verbose=False)

    @staticmethod
    def _redirect_logging(module_name):
        import logging
        from azure.cli.core.azlogging import CustomStreamHandler
        profile_logger = logging.getLogger(module_name)
        if not profile_logger.handlers:
            profile_logger.addHandler(CustomStreamHandler(logging.DEBUG, {
                True: '%(message)s',
                False: '%(levelname)s: %(message)s',
            }))

    @staticmethod
    def _save_file(code, opts, namespace):
        # read arguments
        opts.merge(Struct(f=None))
        file_name = opts.f

        if not file_name:
            return "Usage: %%save_file -f file_name"

        file_name = file_name[0]

        with open(file_name, 'w') as fileName:
            fileName.write(code)

        print("Saved cell to {}".format(file_name))
        return

    @staticmethod
    def easy_reload(module):
        try:
            # python 3.4+ import
            from importlib import reload
        except ImportError:
            try:
                # 3 < 3.4
                from imp import reload
            except ImportError:
                pass
                # builtin for p2

        reload(module)


from IPython import get_ipython

get_ipython().register_magics(AMLHelpers)
