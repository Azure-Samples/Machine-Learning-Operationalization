# Frequently Asked Questions and Known Issues for the AML CLI

This document addresses Frequently Asked Questions and Known Issues with the AML CLI.

## Frequently Asked Questions

**What is the AML CLI?**

The Azure Machine Learning CLI is Azure Machine Learning's new command line experience for deploying Machine Learning models as web services. It is provided as part of the Linux Data Science virtual machine on Azure, and supports deployment of web services to local machines or to Azure clusters.

**Can I run a Docker image that was created using the Azure Machine Learning CLI on another host?**

When you use the CLI to create a web service, it creates a docker image containing the web service and the dependent libraries. The CLI then returns the path to the Docker image file in ACR.

You can use the returned ACR path to deploy the image as a web service on any docker host. 

**How can I check the version of my installed CLI?**
Can you check the version of your CLI using the below command:

	pip show azure-cli-ml

**How do I upgrade just the AML CLI?**

You can upgrade your azuremlcli installation using pip.

To perform the upgrade you must be running as sudo:

	$ sudo -i

Then issue the following command:

	# wget -q https://raw.githubusercontent.com/Azure/Machine-Learning-Operationalization/master/scripts/amlupdate.sh -O - | sudo bash -

**Does the web service support multiple inputs or parse different inputs?**
Yes, it can process multiple inputs packaged in the same JSON request.

**Is the call activated by a  request to the web service a blocking call or an asynchronous call?**
It is blocking/sync. It is expected to be a realtime response. Although, on the client side, you can call it using async http library.

**How many requests can the web service simultaneously handle?**
A lot! It really depends on the size of the cluster and web service itself. You can scale out your service to 100x of PODs and it will handle as many requests concurrently. 

**How many requests can the web service queue up?**
It is configurable. By default it will be set to ~50 per single POD, but you can increase/decrease it to your application requirements. Typically increasing it, increases the service throughput, but makes the latencies worse at higher percentiles. To keep the latencies consistent, you may want to set the queuing to a low value (1-10) and increase the number of PODs to handle the throughput or turn on autoscaling. 

**Can the same machine or cluster be used for multiple web service endpoints?**
Absolutely. You can run 100x of services/endpoints on the same cluster. 
