# Operationalizing ML Models on Azure (Preview)
## Overview

You can efficiently operationalize Spark, Tensorflow, CNTK, or Python based machine learning models using the Azure Machine Learning CLI.

## Getting Started

### Windows

Install Python from [https://www.python.org/](https://www.python.org/). Ensure that you have selected to install pip.

Open a command prompt using Run As Administrator and run the following commands:

    pip install azure-cli
    pip install azure-cli-ml

### Linux

The easiest and quickest way to get started is to use the Data Science VM (see [Provision the Data Science Virtual Machine for Linux (Ubuntu)](https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-dsvm-ubuntu-intro)).

**Note**: The information in this document pertains to DSVMs provisioned after May 1st, 2017.

Once you have provisioned and signed into the DSVM, run the following commands and follow the prompts:

    $ wget -q https://raw.githubusercontent.com/Azure/Machine-Learning-Operationalization/master/scripts/amlupdate.sh -O - | sudo bash -
    $ sudo /opt/microsoft/azureml/initial_setup.sh
    
**NOTE**: You may need to use the sudo -i command first.

**NOTE**: You must log out and log back in to your SSH session for the changes to take effect.


## Set up the Azure Machine Learning environment on Windows and Linux

The cluster environment setup command creates the following resources in your subscription:

* A resource group
* A storage account
* An Azure Container Registry (ACR)
* A Kubernetes deployment on an Azure Container Service (ACS) cluster
* Application insights

**NOTE**: The following items when completing the environment setup:

* You will be prompted to sign in to Azure. To sign in, use a web browser to open the page https://aka.ms/devicelogin and enter the provided code to authenticate.
* During the authentication process you will be prompted for an account to authenticate with. **Important**: Select an account that has a valid Azure subscription and sufficient permissions to create resources in the account.
* When the sign in is complete your subscription information will be presented and you will be prompted whether you wish to continue with the selected account.

To setup the AML environment, on either Windows or Linux, run the following command:

    az ml env setup -c
    
The resource group, storage account, and ACR are created quickly. The ACS deployment can take some time. Once the setup command has finished setting up the resource group, storage account, and ACR, it outputs environment export commands for the AML CLI environment. 

**Note**: If you do not supply a -c or -m parameter when you call the environment set up, the environment is configured a local only mode. If you choose this option, you will not be able to run any cluster mode commands.

The setup command saves a file in your home directory that contains commands to configure your environment. You must run these commands before you use the Azure Machine Learning CLI to operationalize your models.

### Windows 

The environment set commands are saved to:

    C:\users\<user name>\.amlenvrc
    
To set the environment commands temporarily, you can open the file in a text editor, copy the commands, and run them at the command prompt.

To set them permanantly, open your **Control Panel** and click **System**. Next, click **Advanced System Settings** and select the **Advanced** tab. Click **Environment Variables** and add the each of the variables to the **Systems variables**.

### Linux

The environment export commands are saved to:

    ~/.amlenvrc

Source the file to set up your environment variables: 

    $ source ~/.amlenvrc
    
To always set these variables when you log in, copy the export commands into your .bashrc file:

    $ cat < ~/.amlenvrc >> ~/.bashrc
    

