# AML CLI tutorial setup

To complete the AML CLI tutorials, you must provision a Microsoft Linux Data Science Virtual Machine (DSVM). For information on provisioning a DSVM, see [Provision the Linux Data Science Virtual Machine](https://docs.microsoft.com/en-us/azure/machine-learning/machine-learning-data-science-linux-dsvm-intro).

If you have previously provisioned a DSVM and setup the AML CLI environment, you want to ensure that you have the latest AML CLI bits by updating the Updating the CLI. For information on updating the AML CLI installation, see Updating the CLI at the end of this article.

**NOTE**: The information in this document pertains to DSVMs provisioned after February 1st, 2017.

To configure the AML CLI environment sign into the DSVM, run the following commands and follow the prompts:

	$ wget -q http://amlsamples.blob.core.windows.net/scripts/amlupdate.sh -O - | sudo bash -
	$ sudo /opt/microsoft/azureml/initial\_setup.sh

**NOTE**: You must log out and log back in to your SSH session for the changes to take effect.

Next, enter the AML environment setup command. **NOTE**: The following items are important when completing the environment setup:

-   Enter a name for the environment. Environment names must be 20 or fewer characters in length and can only consist of numbers and lowercase letters.

-   You will be prompted to sign in to Azure. To sign in, use a web browser to open the page <https://aka.ms/devicelogin> and enter the provided code to authenticate.

-   During the authentication process you are prompted for an account to authenticate with. Use the account under which you created the DSVM.

-   When the sign in is complete, your subscription information is presented and you are prompted whether you wish to continue with the selected account.

Environment setup command:

	$ aml env setup

Once the setup command has finished, it outputs environment export commands for the AML CLI environment. It also saves these export commands to a file in your home directory. Source the file to set up your environment variables:

	$ source ~/.amlenvrc

To always set these variables when you log in, copy the export commands into your *.bashrc* file:

	$ cat < ~/.amlenvrc >> ~/.bashrc

## Updating the AML CLI Installation

You can update your Azure ML CLI installation using pip.

To perform the update, you must be running as sudo:

	$ sudo -i

Then issue the following command:

	# pip install --upgrade azuremlcli
