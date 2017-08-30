# Operationalizing ML Models on Azure (Preview)
## Overview

This guide gets you started with using the Azure ML CLIs to deploy and manage your machine learning models. To get the most out of this guide, you should have owner access to an Azure subscription that you can deploy your models to.

Using the CLIs, you can efficiently operationalize Spark, Keras, Tensorflow, CNTK, or Python based machine learning models. By the end of this document, you should be able to have your operationalization environment set up and ready for deploying your machine learning models.

For more on operationlaziation, see the [Overview Document](https://github.com/Azure/Machine-Learning-Operationalization/blob/master/documentation/operationalization-overview.md).

## Getting Started
### Accessing the CLIs
_Note: The latest changes to the CLIs require your Azure subscription to be whitelisted before you can start the environment provisioning process. Please contact the Azure ML team's deployml alias with your subscription id before using the CLIs._

The CLIs come pre-installed on the Azure ML App and on Azure DSVMs [https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-virtual-machine-overview]. 

To use the CLIs, on the Azure ML App menu, use File -> Open CommandLine Interface. On a DSVM, open a command prompt. Once there, type *az ml -h* to see the options. For more details, use the --help with individual commands or see the CLI Reference Guide.

On all other systems, you would have to install the CLIs. 

#### Installing (or updating) on Windows

Install Python from [https://www.python.org/](https://www.python.org/). Ensure that you have selected to install pip.

Open a command prompt using Run As Administrator and run the following commands:

    pip install azure-cli
    pip install azure-cli-ml

#### Installing (or updating) on Linux

The easiest and quickest way to get started on Linux is to use the Data Science VM (see [Provision the Data Science Virtual Machine for Linux (Ubuntu)](https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-dsvm-ubuntu-intro)).

**Note**: The information in this document pertains to DSVMs provisioned after May 1st, 2017.

Once you have provisioned and signed into the DSVM, run the following commands and follow the prompts:
 
    $ wget -q https://raw.githubusercontent.com/Azure/Machine-Learning-Operationalization/master/scripts/amlupdate.sh -O - | sudo bash -
    $ sudo /opt/microsoft/azureml/initial_setup.sh
    
**NOTE**: You may need to use the sudo -i command first.

**NOTE**: You must log out and log back in to your SSH session for the changes to take effect.

**NOTE**: You can use the above commands to update an earlier version of the CLIs on the DSVM.

### Deploying web services
Use the CLIs to deploy models as web services. The web services can be deployed locally or to a cluster.

It is recommended to start with a local deployment, validate that your model and code work, then deploy to a cluster for production scale use.

Next, you need to set up the environment. The environment setup is a one time task. Once the setup is complete, you can re-use the environment for subsequent deployments by setting your environment for deployment (see below for more detail).

**NOTE**: The following items when completing the environment setup:

* You will be prompted to sign in to Azure. To sign in, use a web browser to open the page https://aka.ms/devicelogin and enter the provided code to authenticate.
* During the authentication process you will be prompted for an account to authenticate with. **Important**: Select an account that has a valid Azure subscription and sufficient permissions to create resources in the account.
* When the sign in is complete your subscription information will be presented and you will be prompted whether you wish to continue with the selected account.

#### Local deployment (Windows and Linux)
##### Set up the environment
To deploy and test your web service on the local machine, set up a local environment.

    az ml env setup

The local environment setup command creates the following resources in your subscription:

* A resource group
* A storage account
* An Azure Container Registry (ACR)
* Application insights

In local mode only, the setup command saves a file in your home directory that contains environment settings parameters to configure your environment. You must set those environment variables before you use the Azure Machine Learning CLI to operationalize your models. (see below)

*Windows*

The environment set commands are saved to:

    C:\users\<user name>\.amlenvrc
    
To set the environment commands temporarily, you can open the file in a text editor, copy the commands, and run them at the command prompt.

To set them permanently, open your **Control Panel** and click **System**. Next, click **Advanced System Settings** and select the **Advanced** tab. Click **Environment Variables** and add the each of the variables to the **Systems variables**.

*Linux*

The environment export commands are saved to:

    ~/.amlenvrc

Source the file to set up your environment variables: 

    $ source ~/.amlenvrc
    
To always set these variables when you log in, copy the export commands into your .bashrc file:

    $ cat < ~/.amlenvrc >> ~/.bashrc

#### Cluster deployment (Windows and Linux)
##### Set up the environment
To deploy your web service to a production environment, first set up the environment using the following command.

    az ml env setup -c --cluster-name [your environment name] --location [Azure region e.g. eastus]

The cluster environment setup command creates the following resources in your subscription:

* A resource group
* A storage account
* An Azure Container Registry (ACR)
* A Kubernetes deployment on an Azure Container Service (ACS) cluster
* Application insights
   
The resource group, storage account, and ACR are created quickly. The ACS deployment can take some time. Once the setup command has finished setting up the resource group, storage account, and ACR, it outputs environment export commands for the AML CLI environment. 

**NOTE**: If you do not supply a -c parameter when you call the environment set up, the environment is configured a local only mode. If you choose this option, you will not be able to run any cluster mode commands.

After setup is complete, set the environment to be used for this deployment.

    az ml env set --cluster-name [environment name] -g [resource group]
    
- Cluster name: the name used when setting up the environment
- Resource group name: the name you specified for the setup command above. Or if you didn't specify it at time of set up, it was created and returned in the output of the set up command.

Note that once the environment is created, for subsequent deployments, you only need to use the set command above.

##### Create an account
This creates and sets the account that will be used for billing. You need to this once, and can re-use the same account in multiple deployments.

    az ml account modelmanagement create -l [Azure region, e.g. eastus2] -n [your account name] -g [resource group name: existing] --sku-capacity 1 --sku-name S1

The above command also sets the account for deployment which means you can now deploy your web service. For any subsequent deployments however, you need to set the account first using the below command:

    az ml account modelmanagement set -n [your account name] -g [resource group it was created in]

##### Deploy your model
You are now ready to deploy your saved model as a web service. You can start from one of many samples in the gallery or in the samples folder. 

The command to use is as follows:

    az ml service create realtime --model-file [model file/folder path] -f [scoring file e.g. score.py] -n [service name] -s [schema file e.g. service_schema.json] -r [runtime for the Docker container e.g. spark-py]

##### Next Steps

Try one of the many samples in the [samples folder](https://github.com/Azure/Machine-Learning-Operationalization/tree/master/samples).
