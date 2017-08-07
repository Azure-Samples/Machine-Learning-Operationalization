#!/bin/bash

#########################################################################################################
#
# CLI setup
#
#########################################################################################################

## Install AML CLI
echo "Installing Azure Machine Learning Command Line Tools"

## First upgrade pip and setuptools to avoid running into this issue:
## https://github.com/GoogleCloudPlatform/google-cloud-python/issues/2990
/anaconda/envs/py35/bin/pip install pip setuptools --upgrade
/anaconda/bin/pip install pip setuptools --upgrade

## Anaconda Python 3.5
sudo /anaconda/envs/py35/bin/pip install azure-cli-ml --upgrade
sudo /anaconda/envs/py35/bin/pip install azure-cli --upgrade 
sudo /anaconda/envs/py35/bin/pip install azure-cli-core --upgrade

## Anaconda Python 2.7 
sudo /anaconda/bin/pip install azure-cli-ml --upgrade
sudo /anaconda/bin/pip install azure-cli --upgrade
sudo /anaconda/bin/pip install azure-cli-core --upgrade

## reinstall backports, as the --upgrade flag above causes issues
sudo /anaconda/bin/pip uninstall -y backports.shutil-get-terminal-size
sudo /anaconda/bin/pip install backports.shutil-get-terminal-size

USER_HOME=$(getent passwd $SUDO_USER | cut -d: -f6)

## place magic
wget -q https://raw.githubusercontent.com/Azure/Machine-Learning-Operationalization/master/samples/magic/az_ml_magic.py -O ${USER_HOME}/.ipython/profile_default/startup/az_ml_magic.py

## restart kernel
kill $(pgrep -f '/anaconda/bin/python -m ipykernel')

echo "Success."
