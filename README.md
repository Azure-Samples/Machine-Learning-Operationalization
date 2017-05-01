# Operationalizing ML Models on Azure (Preview)

## Overview

You can efficiently operationalize Spark, Tensorflow, CNTK, or Python based machine learning models using the Azure Machine Learning CLI.

## Getting Started

### Windows


Install Python from [https://www.python.org/](https://www.python.org/). Ensure that you have selected to install pip.

Open a command prompt using Run As Administrator and run the following commands:

1. pip install azure-cli
2. pip install azure-cli-ml --upgrade

### Linux

To get started, see [Provision the Linux Data Science Virtual Machine](https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-linux-dsvm-intro).

**Note**: The information in this document pertains to DSVMs provisioned after May 1st, 2017.

Once you have provisioned and signed into the DSVM, run the following commands and follow the prompts:

    $ wget -q http://amlsamples.blob.core.windows.net/scripts/amlupdate.sh -O - | sudo bash -
    $ sudo /opt/microsoft/azureml/initial_setup.sh
    
**NOTE**: You must log out and log back in to your SSH session for the changes to take effect.

Next, set up the Azure Machine Learning (AML) environment. The environment setup command creates the following resources for you:

* A resource group
* A storage account
* An Azure Container Registry (ACR)
* A Kubernetes deployment on an Azure Container Service (ACS) cluster
* Application insights

**NOTE**: The following items when completing the environment setup:

* You will be prompted to sign in to Azure. To sign in, use a web browser to open the page https://aka.ms/devicelogin and enter the provided code to authenticate.
* During the authentication process you will be prompted for an account to authenticate with. Use the account under which you created the DSVM.
* When the sign in is complete your subscription information will be presented and you will be prompted whether you wish to continue with the selected account.

To setup the AML environment, run the following commands:

    $ az ml env setup -k
    
The resource group, storage account, and ACR are created quickly. The ACS deployment can take some time. Once the setup command has finished setting up the resource group, storage account, and ACR, it outputs environment export commands for the AML CLI environment. 

The environment setup saves the set or export commands to a file in your home directory. 

### Windows 

The environment set commands are saved to:

    C:\users\&lt;user name&gt;\.amlenvrc

### Linux

The environment expor commands are saved to:

    ~/.amlenvrc

Source the file to set up your environment variables: 

    $ source ~/.amlenvrc
    
To always set these variables when you log in, copy the export commands into your .bashrc file:

    $ cat < ~/.amlenvrc >> ~/.bashrc
    
