## Tutorial 

The real-time and batch tutorial walk you through building predictive APIs (both realtime and batch) powered by Spark machine learning models, and deploying them to [HDinsight](https://azure.microsoft.com/en-us/services/hdinsight/) and [Azure Container Service](https://azure.microsoft.com/en-us/services/container-service/) clusters for scale.

Additional tutorials are available for:

* [CNTK](samples/cntk/tutorials/realtime)
* [Tensorflow](samples/tensorflow/tutorials/realtime)
* [Python](samples/python/tutorials/realtime) 

## Jupyter notebook

A Jupyter notebooks containing tutorials are available on the DSVM. 

Open Jupyter at https://&lt;machine-ip-address&gt;:8000 in a browser and sign in. The user name and password are those that you configured for the DSVM. Note that you will receive a certificate warning that you can safely click through. 

### Run the Notebook 

There are notebooks for both the real-time and batch web service scenarios. The notebooks are located in the **azureml/realtime** and **azureml/batch** folders. 

To run the real-time scenario, from the azureml folder, change to the realtime folder and open the  realtimewebservices.ipynb notebook. Follow the instructions to train, save, and deploy a model as a real-time web service.  The notebook contains instructions for deploying to the DSVM and for deployment to a production ACS environment.

To run the batch scenario on the DSVM, from the azureml folder, change to the batch folder and open the batchwebservices.ipynb notebook. Follow the provided instructions to train, save, and deploy a model as a local web service to the DSVM or to a production HDInsight environment. 
