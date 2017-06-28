# Operationalizing Batch Processing of Machine Learning Models on Azure (Preview)

You can efficiently operationalize Spark based machine learning models for Batch Process using the Azure Machine Learning CLI. Using the CLI you can deploy models as web services that run on an ACS cluster using Kubernetes.

When you setup your Azure Machine Learning environment, your initial Kubernetes configuration has three worker nodes and a single master. There is a single container per worker node that processes jobs using Spark in standalone mode.

You can submit multiple jobs, and they are queued until a resource to run them becomes available. If you need increased throughput, you can add more nodes through the Kubernetes dashboard.

To access the Kubernetes dashboard:

1. Open a command prompt and enter the following command:

        C:\\<install location>kubectl proxy

2. Copy the returned URL and paste it into a browser, adding /ui to the address.

## Operationalizing a model

First, you must install the Azure Machine Learning CLI and set up an operationalization environment. See the set up instructions in the github repo [Readme](https://aka.ms/o16ncli).

The Azure ML CLI provides deployment environments for local and cluster mode. Batch processing works in cluster mode.

To switch to cluster mode, enter the following command:

    az ml env cluster

To create a web service on the cluster, use the service create command:
--in=--trained-model:food_inspection.model --in=--input-data:wasbs://amlbdpackages@myk8sclusterstor.blob.core.windows.net/food_inspections2.cs
    az ml service create batch -f <scoring file> --in=<input-name-with-leading-dashes>:<default-value> --out=<output-name-with-leading-dashes>:<default-value>  -n <service name>

Example:

    az ml service create batch -f batch\_score.py --in=--trained-model:food\_inspection.model --in=--input-data:food\_inspections2.csv --out=--output-data -n foodinspector

The example command creates a web service named *foodinspector* that uses the scoring file named batch\_score.py. The scoring file defines two inputs and one output; an input for the model, an input for the data, and the output to define the output location. The service is created using the default data from the local file *food\_inspections2.csv* file and no default output location. Any of the inputs and outputs when you run the batch job. 

You can also provide data from remote storage, for example:

* ```az ml service create batch -f batch_score.py --in=--trained-model:food_inspection.model --in=--input-data:https://myk8sclusterstor.blob.core.windows.net/amlbdpackages/food_inspections2.csv --out=--output-data -v -n foodinspector```
* ```az ml service create batch -f batch_score.py v --out=--output-data -v -n foodinspector```

For more information on the scoring file, see [How to create a batch web service for a Spark model on Azure](https://github.com/Azure/Machine-Learning-Operationalization/blob/master/samples/spark/tutorials/batch/batchwebservices.ipynb).

To run a batch job on the web service, use the service run command.

    az ml service run batch -n <service name> -w --in=<input-name-with-leading-dashes>:<value> --out=<output-name-with-leading-dashes>:<value>

Example:

    az ml service run batch --out=--output-data:wasbs://amlbdpackages@myk8sclusterstor.blob.core.windows.net/output.parquet -v -n foodinspector

The example command runs the batch job using the default data supplied when the service was created and specifies an output location for the results. You can override the in data input to score using a different dataset.