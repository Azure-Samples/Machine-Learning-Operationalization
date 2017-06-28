# Installing the machine learning operationalization stack on Ubuntu Linux

Azure Machine Learning operationalization supports deploying models using the following Machine Learning frameworks: SparkML, CNTK, and Python.

SSH into your system and perform the following steps:

1. Install the appropriate prerequisites for the Azure CLI: 

    [Install Azure CLI 2.0](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli#linux-prerequisites)

2. Install pip if it is not already installed:
    
    $ sudo apt-get install python-pip

3. Install Docker community edition. To operationalize models on your local machine, you must install Docker. If you are only operationalizing the models in cluster mode, you can skip step 3, 4, and 5.

    [Docker Community Edition for Ubuntu](https://store.docker.com/editions/community/docker-ce-server-ubuntu)

4. Give the user permissions to run Docker:

    sudo usermod -aG docker $(whoami)

4. Sign out of your session and sign back in.

5. Install the Azure CLI:
 
    sudo pip install azure-cli

6. Install the Azure Machine Learning CLI:
    
    sudo pip install azure-cli-ml --upgrade

When developing code to operationalize a model as a web service, you should use the version of [Python](https://www.python.org/) that matches the version in which your image will run:

* For PySpark solutions, you must use Python 2.7. 
* For all other solutions, use Python 3.5. 

Python 2.7 is the default version of Python and is run when you invoke Python from the command line.  Python 3.x is installed on Ubuntu and is invoked by running python3 at the command line. 

For example, to compile a script file.py using Python 3 you issue the command:
python3 file.py

To invoke python3 when you type python on the terminal, you can use an alias. To add a new alias, open your ~/.bash_aliases file and add the following:

```
alias python=python3
```

Save the file and exit the editor. Source the file with to activate the alias.

```
source ~/.bash_aliases
```
## Set up the Azure Machine Learning environment

The cluster environment setup command creates the following resources in your subscription:

* A resource group
* A storage account
* An Azure Container Registry (ACR)
* A Kubernetes deployment on an Azure Container Service (ACS) cluster
* Application insights

**NOTE**: The following items when completing the environment setup:

* You will be prompted to sign in to Azure. To sign in, use a web browser to open the page https://aka.ms/devicelogin and enter the provided code to authenticate.
* During the authentication process, you will be prompted for an account to authenticate with. **Important**: Select an account that has a valid Azure subscription and sufficient permissions to create resources in the account.
* When the sign in is complete your subscription information will be presented and you will be prompted whether you wish to continue with the selected account.

To setup the AML environment, on either Windows or Linux, run the following command:

    az ml env setup
    
The resource group, storage account, and ACR are created quickly. The ACS deployment can take some time. Once the setup command has finished setting up the resource group, storage account, and ACR, it outputs environment export commands for the AML CLI environment. 

**Note**: If you do not supply a -c or -m parameter when you call the environment set up, the environment is configured a local only mode. If you choose this option, you will not be able to run any cluster mode commands.

The setup command saves a file in your home directory that contains commands to configure your environment. You must run these commands before you use the Azure Machine Learning CLI to operationalize your models.


The environment export commands are saved to:

    ~/.amlenvrc

Source the file to set up your environment variables: 

    $ source ~/.amlenvrc
    
To always set these variables when you log in, copy the export commands into your .bashrc file:

    $ cat < ~/.amlenvrc >> ~/.bashrc