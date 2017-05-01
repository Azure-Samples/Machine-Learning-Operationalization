# Operationalizing ML Models on Azure (Preview)

## Overview

You can efficiently operationalize Spark, Tensorflow, CNTK, or Python based machine learning models using the Azure Machine Learning CLI and a Data Science VM.

The following getting started tutorial walks you through building predictive APIs (both realtime and batch) powered by Spark machine learning models, and deploying them to [HDinsight](https://azure.microsoft.com/en-us/services/hdinsight/) and [Azure Container Service](https://azure.microsoft.com/en-us/services/container-service/) clusters for scale.

Additional tutorials are available for:

* [CNTK](samples/cntk/tutorials/realtime)
* [Tensorflow](samples/tensorflow/tutorials/realtime)
* [Python](samples/python/tutorials/realtime) 

## Getting Started

To get started, see [Provision the Linux Data Science Virtual Machine](https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-linux-dsvm-intro).

**Note**: The information in this document pertains to DSVMs provisioned after May 1st, 2017.

Once you have provisioned and signed into the DSVM, run the following commands and follow the prompts:

	$ wget -q http://amlsamples.blob.core.windows.net/scripts/amlupdate.sh -O - | sudo bash -
	$ sudo /anaconda/envs/py35/bin/pip install azure-cli-ml --upgrade
	$ sudo /opt/microsoft/azureml/initial_setup.sh


**NOTE**: You must log out and log back in to your SSH session for the changes to take effect.

Next, set up the Azure Machine Learning (AML) environment. The environment setup command creates the following resources for you:

* A resource group
* A storage account
* An Azure Container Registry (ACR)
* A Kubernetes deployment on an Azure Container Service (ACS) cluster
* Application insights

**NOTE**: The following items when completing the environment setup:

* You will be prompted to sign in to Azure. To sign in, use a web browser to open the page https://aka.ms/devicelogin and enter the provided code to authenticate.
* During the authentication process you will be prompted for an account to authenticate with. Use the account under which you created the DSVM.
* When the sign in is complete your subscription information will be presented and you will be prompted whether you wish to continue with the selected account.

To setup the AML environment, run the following commands:

	$ az ml env setup -k
	
The resource group, storage account, and ACR are created quickly. The ACS deployment can take some time. Once the setup command has finished setting up the resource group, storage account, and ACR, it outputs environment export commands for the AML CLI environment. 

It saves the export commands to a file in your home directory. Source the file to set up your environment variables: 

	$ source ~/.amlenvrc
	
To always set these variables when you log in, copy the export commands into your .bashrc file:

	$ cat < ~/.amlenvrc >> ~/.bashrc
	
Example status command: 

	az ml env setup -s doncli04082017rgdeploymentacs20170407062300

## Jupyter notebook

A Jupyter notebooks containg tutorials are available on the DSVM. 

Open Jupyter at https://&lt;machine-ip-address&gt;:8000 in a browser and sign in. The user name and password are those that you configured for the DSVM. Note that you will receive a certificate warning that you can safely click through. 

### Run the Notebook 

There are notebooks for both the real-time and batch web service scenarios. The notebooks are located in the **azureml/realtime** and **azureml/batch** folders. 

To run the real-time scenario, from the azureml folder, change to the realtime folder and open the  realtimewebservices.ipynb notebook. Follow the instructions to train, save, and deploy a model as a real-time web service.  The notebook contains instructions for deploying to the DSVM and for deployment to a production ACS environment.

To run the batch scenario on the DSVM, from the azureml folder, change to the batch folder and open the batchwebservices.ipynb notebook. Follow the provided instructions to train, save, and deploy a model as a local web service to the DSVM or to a production HDInsight environment. 

## Updating the DSVM environment

To update the Azure ML bits on the DSVM, run the following command.

	$ wget -q http://amlsamples.blob.core.windows.net/scripts/amlupdate.sh -O - | sudo bash -
