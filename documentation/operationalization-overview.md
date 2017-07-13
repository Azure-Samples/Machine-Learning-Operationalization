Operationalization is the process of publishing models and code as web services, and the consumption of these services to produce business results.

Azure Machine Learning Operationalization is a component of the Azure CLI that enables operationalization of models that use the CNTK, SPARK, and Python machine learning platforms.

You can use the Operationalization CLIs from the Vienna desktop app (File->Open Command-Line Interface) or install the CLIs direclty from the command line.

## Basic Concepts

### Local and cluster modes 

Azure ML Operationalization provides two deployment modes: local and cluster.

Local mode deployments run in docker containers on a single computer, whether that is your personal machine or a VM running on Azure. You can use local mode for development and testing.

In cluster mode, your service is run in Azure Container Service (ACS). The operationalization environment provisions Docker and Kubernetes in the cluster to manage web service deployment. Deploying to ACS allows you to scale your service as needed to meet your business needs.

### Realtime and Batch processing 

Depending on your business needs, you can deploy your service in one of two processing modes:

* Realtime: Provides a web service that you call synchronously to score data on an as-needed basis.
* Batch: Provides a web service that you call asynchronously to score a batch of data records.

### Environment configuration

Before you can operationalize your model, you must configure your environment. 

To configure the machine learning operationalization environment, you must have access to an Azure subscription with sufficient permissions to create Azure assets (e.g. Contributor or Admin access).

By default, the Vienna's environment configuration only supports local deployments. Requirements to run in local mode are:

* Azure CLI version 2.0
* Azure Machine Learning CLI component
* Python 3.5
* Docker

Optionally, you can configure the environment to support cluster deployments. To do this you will need:

* Spark for Spark based models
* Microsoft Cognitive Tool Kit for CNTK-based models

## Creating the Web Service

You can create a new web service in the Azure CLI using the *ml service create* command, which deploys the web service and returns a scoring endpoint URL.

When creating a realtime web service, you must supply a name for the service and a scoring script (sometimes referred to as the driver file.) The scoring script loads the data and runs it against the model to provide predictions.

Additionally, you can specify the following options for a realtime service:

* Files and directories required by the service. 
* Enable [Applications Insights](https://docs.microsoft.com/en-us/azure/application-insights/) logging.
* The model to be deployed.
* A pip requirements.txt file of packages needed by the code file.
* The runtime of the web service. Valid runtimes are spark-py, cntk-py, tensorflow-py, scikit-py. The default runtime is spark-py.
* The input and output schema of the web service.
* Number of nodes for the Kubernetes service in a cluster.  The default is 1.

For a batch web service you can specify the following options:

* Inputs for service to expect.
* Outputs for service to expect.
* Parameters for service to expect.
* The title of service, defaults to service_name.
* Files and directories required by the service. 

### Consuming the web service

Once the web service has been successfully deployed, you can call it using the CLI or by calling the scoring endpoint.

To test or use your new web service, you call it from the Vienna CLI using the *ml service run* command.

For more information on how to consume the web service, see [Consuming your operationalized web service](consume-web-service.md).

## Additional Concepts				
	
### logging
You can troubleshoot your web service by viewing the logs. In local mode, you can inspect the Docker logs to diagnose issues with your deployment.

In cluster mode, you can specify that logging in performed using Azure Application Insights.

For more information on Docker logs, see[Logs and troubleshooting](https://docs.docker.com/docker-for-windows/troubleshoot/) on the Docker web site.

For more information on logging in cluster mode, see [How to enable logging](how-to-enable-logging.md).

### Remote models, input data, and output data

Creating and running a web service in cluster mode uses models and data that is stored remotely. The CLI uses the credentials stored in your environment configuration to access blobs located in Azure storage. The CLI uses the same credentials to store output in blobs in the storage account.

For more information on accessing remote data, see [How to use remotely stored data in a batch service call](how-to-use-remotely-stored-data-in-batch.md) and [Operationalizing Batch Processing of Machine Learning Models on Azure (Preview)](batch-processing.md).

### Scaling your web service

Operationalized models are deployed on ACS clusters on which Kubernetes has been installed, and can be scaled in two ways:

* You can increase the number of agent nodes in the cluster.
* You can increase the number of Kubernetes pods

For more information, see [How to scale operationalization on your ACS cluster](how-to-scale.md).
