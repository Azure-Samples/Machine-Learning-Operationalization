# Installing the operationalization stack on Windows 10 or Windows Server


Azure Machine Learning operationalization supports deploying models using the following Machine Learning frameworks: SparkML, CNTK, and Python.

## Installation

Sign in to your system and perform the following steps:

1. Install the Azure CLI:

    pip install azure-cli

2. Install the Azure Machine Learning CLI component:

    pip install azure-cli-ml --upgrade

When developing code to operationalize a model as a web service, you should use the version of [Python](https://www.python.org/) that matches the version in which your image will run:

* For PySpark solutions, you must use Python 2.7. 
* For all other solutions, use Python 3.5. 

If you develop and test locally with other Python versions, you could encounter unexpected behavior when you publish a web service.

## Set up the Azure Machine Learning environment

The cluster environment setup command creates the following resources in your subscription:

* A resource group
* A storage account
* An Azure Container Registry (ACR)
* A Kubernetes deployment on an Azure Container Service (ACS) cluster
* Application insights

**NOTE**: The following items when completing the environment setup:

* You will be prompted to sign into Azure. To sign in, use a web browser to open the page https://aka.ms/devicelogin and enter the provided code to authenticate.
* During the authentication process, you will be prompted for an account to authenticate with. **Important**: Select an account that has a valid Azure subscription and sufficient permissions to create resources in the account.
* When the sign in is complete your subscription information will be presented and you will be prompted whether you wish to continue with the selected account.

To setup the AML environment, on either Windows or Linux, run the following command:

    az ml env setup -c
    
The resource group, storage account, and ACR are created quickly. The ACS deployment can take some time. Once the setup command has finished setting up the resource group, storage account, and ACR, it outputs environment export commands for the AML CLI environment. 

**Note**: If you do not supply a -c or -m parameter when you call the environment set up, the environment is configured a local only mode. If you choose this option, you will not be able to run any cluster mode commands.

The setup command saves a file in your home directory that contains commands to configure your environment. You must run these commands before you use the Azure Machine Learning CLI to operationalize your models.

The environment set commands are saved to:

    C:\users\<user name>\.amlenvrc
    
To temporarily set the environment commands, rename the ```.amlenvrc``` file to ```amlenvrc.cmd``` and run it at the command prompt.

To set them permanently, open your **Control Panel** and click **System**. Next, click **Advanced System Settings** and select the **Advanced** tab. Click **Environment Variables** and add the each of the variables to the **Systems variables**.