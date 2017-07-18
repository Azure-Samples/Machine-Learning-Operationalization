# Frequently Asked Questions and Known Issues for the AML CLI

This document addresses Frequently Asked Questions and Known Issues with the AML CLI.

## Frequently Asked Questions

**What is the AML CLI?**

The Azure Machine Learning CLI is Azure Machine Learning's new command line experience for deploying Machine Learning models as web services. It is provided as part of the Linux Data Science virtual machine on Azure, and supports deployment of web services to local machines or to Azure clusters.

**Can I run a Docker image that was created using the Azure Machine Learning CLI on another host?**

When you use the CLI to create a web service, it creates a docker image containing the web service and the dependent libraries. The CLI then returns the path to the Docker image file.

You can use the returned path to deploy the image as a web service on any docker host. 

**How do I upgrade just the AML CLI?**

You can upgrade your azuremlcli installation using pip.

To perform the upgrade you must be running as sudo:

	$ sudo -i

Then issue the following command:

	# wget -q https://raw.githubusercontent.com/Azure/Machine-Learning-Operationalization/master/scripts/amlupdate.sh -O - | sudo bash -


## Known Issues

**Creating a web service in cluster mode takes a long time.**

Deploying a real-time web service in the cluster environment can take a very long time. During deployment you may receive an error similar to the following sample. 

	$ aml service create realtime -f testing.py -m housing1.model -s webserviceschema.json -n mytestapp
	Uploading dependencies.
	/anaconda/envs/py35/lib/python3.5/site-packages/azuremlcli/azuremlutilities.py
	Creating docker image...done.
	Image available at : yammesacr-microsoft.azurecr.io/mytestapp
	Error creating service.
	b'{"version":"2017-02-28T05:10:15.963Z","deploymentId":"a106fd55-a7de-f1f2-b9ba-1bbbccceb531"}'

This can happen of the first deployment to the cluster when all layers necessary for the deployment are being retrieved. If you run the service list command, you may see the service in a status of *Deploying* and *Unhealthy*. Deploying indicates that the container has not yet started; either because there are no resources available to run the container, or the image is still being retrieve. The status will change to *Running* and *Healthy* if you have sufficient resources to deploy the web service, and there are no errors in your web service script.
