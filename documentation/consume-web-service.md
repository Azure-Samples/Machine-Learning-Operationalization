# Consuming the web service

When the web service is succesffuly deployed, you can call it using the CLI or by calling the scoring endpoint.

The CLI provides the *ml service run*  command which you can use to test your web service. 

The basic realtime service run command take the name of the web service as the input and calls the web service using default data supplied when you created the service.

```
az ml service run realtime -n <service name>
```

Optionally, if you did not provide default data or you want to test with alternate data, you can specify data with which to test.

```
az ml service run realtime -n <service name> [-d "\"YOUR DATA HERE\""]
```
NOTE: When specify data to test with, do not include the brackets - [].

When calling a batch web service, you must supplye service name and a location for the output. Optionally, you can also specify a model to use, input data to evaluate, and an ID for the job.

```
az ml service run batch -n <service name>  --out=--output-data:<value> [--in=--trained-model:<value>] [--in=--input-data:<value>] [-j <job_id>]
```
NOTE: When include optional parameters to the command, do not include the brackets - [].

You can also use CURL to call and test your web service. When using CURL you are calling the scoring endpoint that is returned when you deploy the web service..

```
  curl : curl -X POST -H "Content-Type:application/json" --data "\"YOUR DATA HERE]" http://<host address>:80/api/v1/service/<service name>/score
```

For sample code showing how to call the web service from C#, see:

* [CLIClientConsoleApp](https://github.com/Azure/Machine-Learning-Operationalization/tree/master/samples/python/tutorials/Sample%20C%23%20Client%20App/CLIClientConsoleApp)
* [Call an operationalized Microsoft Cognitive Toolkit model from an Android app](https://gallery.cortanaintelligence.com/Tutorial/Call-an-operationalized-Microsoft-Cognitive-Toolkit-model-from-an-Android-app)