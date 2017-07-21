# Installing the operationalization stack on Windows 10 or Windows Server


Azure Machine Learning operationalization supports deploying models using the following Machine Learning frameworks: SparkML, CNTK, and Python.

## Installation

Sign in to your system and perform the following steps:

1. Install the Azure CLI:

    pip install azure-cli

2. Install the Azure Machine Learning CLI component:

    pip install azure-cli-ml --upgrade

Install Python 3.5 [Python](https://www.python.org/).

If you develop and test locally with other Python versions, you could encounter unexpected behavior when you publish a web service.

To run deploy models as a web service to your local machine, you must install [Docker for Windows](https://docs.docker.com/docker-for-windows/).

## Set up the Azure Machine Learning environment for local mode deployment

The cluster environment setup command creates the following resources in your subscription:

* A resource group
* A storage account
* An Azure Container Registry (ACR)
* Application insights

**Important**: During the environment setup:

* You  are prompted to sign into Azure. To sign in, use a web browser to open the page https://aka.ms/devicelogin and enter the provided code to authenticate.
* During the authentication process, you are prompted for an account to authenticate with. **Important**: Select an account that has a valid Azure subscription and sufficient permissions to create resources in the account.
* When the sign in is complete your subscription information is presented and you are prompted whether you wish to continue with the selected account.

To setup the AML environment run the following command:

```
    az ml env setup 
```

Once the setup command has finished setting up the resource group, storage account, and ACR, it outputs environment export commands for the AML CLI environment. 

**Note**: If you do not supply a -c or -m parameter when you call the environment set up, the environment is configured a local only mode. If you choose this option, you will not be able to run any cluster mode commands.

The setup command saves a file in your home directory that contains commands to configure your environment. You must run these commands before you use the Azure Machine Learning CLI to operationalize your models.

The environment set commands are saved to:

    C:\users\<user name>\.amlenvrc.cmd
    
To temporarily set the environment commands, run the ```amlenvrc.cmd``` file at the command prompt.

To set them permanently, open your **Control Panel** and click **System**. Next, click **Advanced System Settings** and select the **Advanced** tab. Click **Environment Variables** and add the each of the variables to the **Systems variables**.

## Set up to deploy to an ACS cluster

In cluster mode, web services are deployed to an Azure Container Service (ACS) cluster on which Kubernetes is deployed.

To set up the operationalzation environment to create the ACS cluster and deploy the  to run in cluster mode, 
```
    az ml env setup -c
```

To change to cluster mode, run the following command:

```
az ml env cluster
```
