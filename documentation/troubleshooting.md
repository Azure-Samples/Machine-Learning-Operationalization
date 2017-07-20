# Troubleshooting web services
During deployment or when calling the web service, you can use the following resources to determine the cause of the errors.

## Troubleshooting

### 1. Docker logs

After using the "service create" command, a docker container is created to package the model and its dependencies for deployment. You can find this container, and view its log by using the following. Look for the image that has the name of your service.

- docker ps

If the above does not show your container, try:

- docker ps -a

Then use the container Id in the following call:

- docker logs <containerid>

### 2. Kubernetes logs

If you deployed your web service to an ACS cluster, then you can view the Kubernetes logs. To access the logs, you need to use the kubectl tool to access the Kuberentes UI. In Windows, the tool is noramlly installed to the c:\users\<username>\bin folder.

To access it, type the following:

c:\users\<username>bin>kubectl proxy

Then browse to the specified address (127.0.0.1:8001/ui). Once there, click on Pods, then on the hamburger icon for your service.


## 3. App Insights

If you use the "-l" flag without the quotes when deploying a web service, then the service logs are written to the App Insights instance for your environment in Azure. You can search for it using the environment name you used when using the az ml env setup command.

To access it:

- Use -l when creating service
- Open App Insights in Azure Portal. Use the environment to find the App Insights instance.
- Once in App Insights, click on Search in the top menu to view the results
- Or go to Analytics ->Exceptions > exceptions take | 10