# Frequently Asked Questions and Known Issues for the AML CLI

This document addresses Frequently Asked Questions and Known Issues with the AML CLI.

## Frequently Asked Questions

**What is the AML CLI?**

The Azure Machine Learning CLI is Azure Machine Learning's new command line experience for deploying Machine Learning models as web services. It is provided as part of the Linux Data Science virtual machine on Azure, and supports deployment of web services to local machines or to Azure clusters.

**Can I run a Docker image that was created using the Azure Machine Learning CLI on another host?**

When you use the CLI to create a web service, it creates a docker image containing the web service and the dependent libraries. The CLI then returns the path to the Docker image file.

You can use the returned path to deploy the image as a web service on any docker host. 

**How do I upgrade just the AML CLI?**

You can upgrade your azuremlcli installation using pip.

To perform the upgrade you must be running as sudo:

	$ sudo -i

Then issue the following command:

	# wget -q https://raw.githubusercontent.com/Azure/Machine-Learning-Operationalization/master/scripts/amlupdate.sh -O - | sudo bash -
