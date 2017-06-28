# How to operationalize a remotely stored model

When you create your web service, you can use a model that is stored in a private blob in Azure storage. When using this scenario, the blob must be in the storage account that was created during your environment setup and that setup must be the active one in your az ml CLI environment. When you create the service the CLI uses the credentials stored in your environment to retrieve the model.

You can upload the model to your azure storage account using any of the following methods:

* [Azure Storage explorer](http://storageexplorer.com/)
* [AZCopy](https://docs.microsoft.com/en-us/azure/storage/storage-use-azcopy)
* Directly through the [Azure portal](https://portal.azure.com)

To find the name of the storage account, open your .amlenvrc file and find the *AML_STORAGE_ACCT_NAME* variable.

The command to create a web service using remote data takes the following form:

     az ml service create batch -f <myfile>.py --in=--trained-model:<mytrainedmodel> --in=--input-data:<protocol>://<mycluster>.blob.core.windows.net/<mypackages>/<myfile>.csv --out=--output-data -v -n <myservicename> 

The following is an example CLI command to create a service using a model stored in a private Azure blob:

    az ml service create realtime -r cntk-py -f driver.py -m https://donsubuncli06012017stor.blob.core.windows.net/models/resnet.dnn -n cntksrvc2

You can specify either a https or wasb url to the model.