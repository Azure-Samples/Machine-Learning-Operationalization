# Azure machine learning CLI tutorial setup

To complete the Azure machine learning CLI tutorials, you must provision a Data Science Virtual Machine (DSVM). 

If you have previously provisioned a DSVM and setup the CLI environment, you want to ensure that you have the latest CLI bits by updating the Updating the CLI. For information on updating the CLI installation, see Updating the CLI at the end of this article.

To get started, see [Provision the Linux Data Science Virtual Machine](https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-linux-dsvm-intro).

**Note**: The information in this document pertains to DSVMs provisioned after May 1st, 2017.

Once you have provisioned and signed into the DSVM, run the following commands and follow the prompts:

	$ wget -q http://amlsamples.blob.core.windows.net/scripts/amlupdate.sh -O - | sudo bash -
	$ sudo /anaconda/envs/py35/bin/pip install azure-cli-ml --upgrade
	$ sudo /opt/microsoft/azureml/initial_setup.sh

**NOTE**: You must log out and log back in to your SSH session for the changes to take effect.

Next, enter the environment setup command. **NOTE**: The following items are important when completing the environment setup:

-   You will be prompted to sign in to Azure. To sign in, use a web browser to open the page <https://aka.ms/devicelogin> and enter the provided code to authenticate.
-   During the authentication process you are prompted for an account to authenticate with. Use the account under which you created the DSVM.
-   When the sign in is complete, your subscription information is presented and you are prompted whether you wish to continue with the selected account.

Environment setup command:

	$ az ml env setup -k

Once the setup command has finished, it outputs environment export commands for the AML CLI environment. It also saves these export commands to a file in your home directory. Source the file to set up your environment variables:

	$ source ~/.amlenvrc

To always set these variables when you log in, copy the export commands into your *.bashrc* file:

	$ cat < ~/.amlenvrc >> ~/.bashrc

## Updating the AML CLI Installation


You can upgrade your Azure ml CLI component using pip.

To perform the upgrade you must be running as sudo:

	$ sudo -i

Then issue the following command:

	# pip install --upgrade azure-cli-ml

