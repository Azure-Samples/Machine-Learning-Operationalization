# How to use remotely stored data in a batch service call

When you run your batch web service, you can specify data that is stored in a private blob in Azure storage. When using this scenario, the blob must be in the storage account that was created during your environment setup and that setup must be the active one in your az ml CLI environment. When you create the service the CLI uses the credentials stored in your environment to retrieve the data.

You can upload the data to your Azure storage account using any of the following methods:

* [Azure Storage explorer](http://storageexplorer.com/)
* [AZCopy](https://docs.microsoft.com/en-us/azure/storage/storage-use-azcopy)
* Directly through the [Azure portal](https://portal.azure.com)

To find the name of the storage account, open your .amlenvrc file and find the *AML_STORAGE_ACCT_NAME* variable.

The command to run a web service using remote data takes the following form:

     az ml service run batch --in=--input-data:<protocol>://<mycluster>.blob.core.windows.net/<mypackages>/<myfile>.csv --out=--output-data:<mycluster>.blob.core.windows.net/<mypackages>/<myfile> -v -n <myservicename>

The following is an example CLI command to run a service using data stored in a private Azure blob:

     az ml service run batch --in=--input-data:https://myk8sclusterstor.blob.core.windows.net/amlbdpackages/food_inspections2.csv --out=--output-data:wasbs://amlbdpackages@myk8sclusterstor.blob.core.windows.net/output.parquet -v -n foodinspector