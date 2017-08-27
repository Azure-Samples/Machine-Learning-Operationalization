# How to create the score.py file

To deploy your model as a web service, you need to create a score.py file. This file will be packaged along with your model and, optionally, a schema file as part of the deployment process.

This file should include two functions: init and run.

## The init function
The init function loads the saved model. 

This requires the model to be saved to a file (e.g. pkl) after it has been trained - and before it can be loaded into init().

Example of init function:

```python
def init():   
    from sklearn.externals import joblib
    global model
    model = joblib.load('model.pkl')
```
## The run function
The run function uses the model and the input data to return a prediction.

Example of run function for taking input and returning a prediction:

```python
def run(input_data):
    try:
        prediction = model.predict(input_data)
        return prediction
    except Exception as e:
        return (str(e))
```
## Creating socre.py

You can combine the above two functions and save them in a file called score.py. And you would have this necessary piece of the model deployment process.

If you are using a Jupyter notebook with Python 3, you can use the _%%writefile_ Magic command the top of the cell containing the two functions. Running that cell will save the file.

```
%%writefile score.py
init()
...
run(input_data)
...
```
See this [sample](https://github.com/Azure/Machine-Learning-Operationalization/blob/master/samples/python/tutorials/realtime/digit_classification.ipynb) for an example of the above.

## Best practices

- The model should be loaded locally in the init function. It is NOT recommended to load the model from remote storage in init().
