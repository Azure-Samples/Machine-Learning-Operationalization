In this tutorial, you will learn how to deploy a Microsoft Cognitive Toolkit (CNTK) model as a web service using the Azure Machine Learning component for the Azure CLI 2.0. The tutorial is based on the (CNTK) Hands On Lab for Image Recognition ([*CNTK 201B: Hands On Labs Image Recognition*](https://github.com/Microsoft/CNTK/blob/v2.0.beta12.0/Tutorials/CNTK_201B_CIFAR-10_ImageHandsOn.ipynb)) and uses the CIFAR dataset from CNTK wiki notebook samples found in the CNTK tutorials ([*https://github.com/Microsoft/CNTK/tree/v2.0.beta12.0/Tutorials*](https://github.com/Microsoft/CNTK/tree/v2.0.beta12.0/Tutorials)).

Steps:

1. Provisions the DSVM.  
3. Upload the trained model to the DSVM.
2. Create the web Service.

To complete the CLI tutorials and walkthroughs, you must provision a Data Science Virtual Machine (DSVM). If you have not yet provisioned a DSVM, see the [tutorial setup](../../../tutorial_setup.md) document.

## About the model

For the purposes of the tutorial we have pretrained a model and made it available, along with the necessary supporting files, on GitHub in the files folder of this tutorial. For information on how the model was trained, see the notes at the end of this tutorial.

## Upload the trained Model

To use the pretrained model, sign in to you DSVM. Change folders to notebooks &gt; azureml and create a new folder named *cntk*. Open the files folder of this tutorial. Copy the *resnet.dnn*, *driver.py*, and *score\_file.py* files from GitHub to the cntk folder on the DSVM. Open the images folder and copy the *car.png* to the cntk folder on the DSVM. 

## Deploy the model as web service

To deploy the model as a web service, you must supply a driver program that loads the trained model and scores the input. For this tutorial, you will use the sample *driver.py* that you have copied to the cntk folder on the DSVM.

From the command line on the DSVM, run the CLI service create command to deploy the model as a real-time web service:

	$ aml service create realtime -r <runtime type>  -f <driver file> -m <model file> -n <your service name>

Example:

	$ aml service create realtime -r cntk-py -f driver.py -m resnet.dnn -n cntksrvc2

When the service finishes deploying, the CLI returns the service URL and service port which you use to call the service. If you need to retrieve the URL and port, you can call the ```aml service view``` command.

	$ aml service view realtime <your service name>

For information on deploying the web service on an ACS cluster, see the notes section at the end of the tutorial.

## Test the web service by scoring an image

Once the web service is deployed, you can call it to classify images in two ways:

1. To score the sample car.png image using Python run the following command:

	$ python score_cntk.py --img car.png --url http://&lt;your service URL&gt;:&lt;your service port&gt;/score --name &lt;your service name&gt;

	Example:

	$ python score\_cntk.py --img car.png --url http://127.0.0.1:32794/score --name cntksrvc2

1.  You can also use an CLI command to score the image. When using the CLI, you must the supply the input image as a base64 string as shown in the following example:

	```
	$ aml service run realtime -n <your service name> -d '{"input": "[\"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\"]"}'
	```
 

## Summary

Using the  Azure Machine Learning component for the Azure CLI 2.0, you can quickly deploy and test a CNTK trained model as a web service. When you are satisfied with the results of your testing and want to scale out the service, you can use the same commands to deploy the web service to an ACS cluster.

## Notes

### Updating the AML CLI Installation

You can upgrade your Azure ml CLI component using pip.

Linux DSVMs

To perform the upgrade you must be running as sudo:

	$ sudo -i

Then issue the following command:

	# pip install --upgrade azure-cli-ml

Windows DSVM

Open a command prompt with the Run as Administrator option.

In the command prompt, issue the following command:

	pip install --upgrade azure-cli-ml

### Deploying to an ACS cluster

A three node ACS is cluster is provisioned as part of the *aml env setup*. The provisioning takes about 20 minutes and updates the *.amlenvrc* file with the information on the cluster.

Source the file to set up your environment variables that include the ACS cluster information:

	$ source ~/.amlenvrc

To set your environment to cluster mode, enter the following command:

	$ az ml env cluster

When the service finishes deploying, the CLI returns the service URL which you use to call the service. If you need to retrieve the URL and port, you can call the ```az ml service view``` command. When you call the web service on the ACS cluster, you must always use port 9091.

You can then run the following command to create the service on the cluster.

	$ az ml service create realtime -r <runtime type>  -f <driver file> -m <model file> -n <your service name>

Example: 

	$ az ml service create realtime -r cntk-py -f driver.py -m resnet.dnn -n cntksrvc2


The To test the web service on the cluster run the python script:

	$ python score_cntk.py --img car.png --url http://<your service URL>:9091/score --name <your service name>

### Training the model

The model contained in the *resnet.dnn* file was trained using sample notebooks from the CNTK tutorials.

1.  The CIFAR-10 Data Loader notebook was used to prepare the images used for training: [https://github.com/Microsoft/CNTK/blob/v2.0.beta12.0/Tutorials/CNTK\_201A\_CIFAR-10\_DataLoader.ipynb](https://github.com/Microsoft/CNTK/blob/v2.0.beta12.0/Tutorials/CNTK_201A_CIFAR-10_DataLoader.ipynb)

2.  The CNTK 201B: Hands On Labs Image Recognition notebook was used to train model:

	[https://github.com/Microsoft/CNTK/blob/v2.0.beta12.0/Tutorials/CNTK\_201B\_CIFAR-10\_ImageHandsOn.ipynb](https://github.com/Microsoft/CNTK/blob/v2.0.beta12.0/Tutorials/CNTK_201B_CIFAR-10_ImageHandsOn.ipynb)
	
	The notebook was modified to save the model to file which can be uploaded to the DSVM.
	
	Following libraries commands were added to the import and the save and reload functions as listed below.

	    		
		from cntk.ops import \*
		from cntk.ops.functions import load_model
		 
		# Save the trained model to file
		mymodel.save_model('mymodel.dnn')
		 
		# Load the model from disk and perform evals
		mymodel_reloaded = load_model('mymodel.dnn')
