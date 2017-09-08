# Iris sample

This sample demonstrates how to train and save a model and deploy it as a web service on your local machine. 
The model is created using the [Iris dataset](http://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html). 

Steps:

1. Set up your environment
2. Train and save the model
3. Create web service
4. Run web service

## Set up your environment

The steps in the sample are intended to be performed on a machine running Windows 10.

To setup your environment for operationalization your local machine, see [Installing the operationalization stack on Windows 10 or Windows Server](https://github.com/Azure/Machine-Learning-Operationalization/blob/master/documentation/install-on-windows.md).

### Set up the machine learning operationalization environment

At the command line enter the following to create a local operationalization environment.

```
az ml env setup -n <environment name> -l <Azure region location>
```

## Use python to train and save the model 

From the sample folder, download the ```iris_train.py``` training file.
Change to your projects folder and train the model by entering the following command.
```
python iris_train.py
```
## Generate the schema
Run the iris_score.py file using the Python command to create a schema file service_schema.json:

```
python iris_score.py
```

## Create the web service

Next, download the iris_scory.py scoring file.
Enter the following command to create the web service on your local machine.
```
az ml service create realtime -f iris_score.py --model-file model.pkl -s service_schema.json -n irisservice1 -r python
```
## Run the service

```
az ml service run realtime -i <service id> -d "{\"input_df\": [{\"sepal length\": 3.0, \"sepal width\": 3.6, \"petal width\": 1.3, \"petal length\":0.25}]}"
```

If you encounter difficulties, see the [Troubleshooting Guide](https://github.com/Azure/Machine-Learning-Operationalization/blob/master/documentation/troubleshooting.md).
