
# How to enable logging

Logging uses the [Application Insights](https://docs.microsoft.com/en-us/azure/application-insights/) service. When you run the service, stdin, stdout, and stderr are captured in the log. It takes five to ten minutes for the logs to show up in the portal.

You must have at least contributor access in the subscription your are using for operationalization.

To enable logging, use the *-l* parameter when you the create service:

    az ml service create realtime -f testing.py -m housing.model -n mytestapp -l

To view the logs:

1. Sign into the [Azure portal](https://portal.azure.com).
2. Click **More Services**.  
3. In the search box, type *app insights* and press **Enter**.
4. From the **Application Insights** search blade, select the Application Insights resource. The name of the service is constructed by taking the resource group name you specified when setting up your machine learning environment and appending "_ins" to it.
5. Click on Overview, then on Search on the menu bar to see the log entries (note that it could take a few minutes before the entries are displayed)
6. You can also see the exception by clicking on Analytics -> exceptiops. Then type in execptions | take 10 and press Go on the top right corner.
