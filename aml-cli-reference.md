# Azure Machine Learning Command Line Tools

You can update your Azure ML CLI installation using pip.

To perform the update, you must be running as sudo:

	$ sudo -i


Then issue the following command:

	# pip install --upgrade azuremlcli


Base commands:

- env: Shows the current Azure ML related environment settings.
- service: Allows you to manage Azure ML web services.

## Environment commands

- aml env setup: Display help on setting up your environment.
- aml env local: Switches your environment to local mode.
- aml env cluster: Switches your environment to cluster mode.

**Environment Setup**

*aml env setup*

Initializes your Azure machine learning environment with a storage account, ACR registry, and ACS cluster.
You are prompted for the following information during the setup:

* A name for your environment. Environment names must between 3 and 20 characters in length and can only consist of numbers and lowercase letters.
* The subscription in which to create Azure resources.

**Local mode**

*aml env local*

In local mode, the CLI creates locally running web services for development
and testing. To run the CLI in local mode, set the following environment variables:

| Variable | Description |
|---|---|
| AML_STORAGE_ACCT_NAME | Set this to an Azure storage account. For more information about Azure storage accounts, see https://docs.microsoft.com/en-us/azure/storage/storage-introduction |                        
| AML_STORAGE_ACCT_KEY | Set this to either the primary or secondary key of the above storage account. |
| AML_ACR_HOME | The URL of your Azure Container Registry (ACR). For more information about the Azure Container Registry, see https://docs.microsoft.com/en-us/azure/container-registry/container-registry-intro |
| AML_ACR_USER | The username of the ACR specified by AML_ACR_HOME. |
| AML_ACR_PW  | The password of the ACR specified by AML_ACR_HOME. |

**Cluster mode**

*aml env cluster*

In cluster mode, the CLI is used to deploy production web services. Real-time web services are deployed to
an Azure Container Service (ACS) cluster, and batch web services are deployed to an HDInsight Spark cluster. 
For more information on ACS, see https://docs.microsoft.com/en-us/azure/container-service/container-service-intro.

To use the CLI in cluster mode, define the following environment variables (in addition to those above for
local mode):

| Variable | Description |
|---|---|
| AML_ACS_MASTER | Set this to the URL of your ACS Master (e.g.yourclustermgmt.westus.cloudapp.azure.com) |
| AML_ACS_MASTER_PORT | If port forwarding is set for the ACS cluster, set this to the local port that is forwarded to port 80 on the ACS master. For details on setting up port forwarding, see https://docs.microsoft.com/en-us/azure/container-service/container-service-connect. If this is set, AML defaults to localhost to communicate with ACS and AML_ACS_MASTER is ignored. |
| AML_ACS_AGENT  | Set this to the URL of your ACS Public Agent (e.g. yourclusteragents.westus.cloudapp.azure.com) |
| AML_HDI_CLUSTER  | Set this to the URL of your HDInsight Spark cluster. |
| AML_HDI_USER  | Set this to the admin user of your HDInsight Spark cluster. |
| AML_HDI_PW  | Set this to the password of the admin user of your HDInsight Spark cluster. |


*aml env local*

Switches to the local deployment environment. 

*aml env cluster [-f]*

Switches to the local deployment environment. Use the -f flag to force a switch to the cluster environment.


------------------------------------------------------------------------------
## Service commands

The following command perform the action for web services in the current, local or cluster, environment.

* aml service list: Lists the AML web services.
* aml service create: Creates a new AML web service.
* aml service run: Runs an existing AML web service.
* aml service view: Retrieves the status an existing AML web service.
* aml service scale: Scale an existing AML real-time web service.
* aml service listjobs: Lists the jobs on an existing AML batch web service.
* aml service viewjob: Retrieves the status of job on and existing AML batch web service.
* aml service canceljob: Cancels a job on an existing AML batch web service.
* aml service delete: Deletes an existing AML web service.


*aml service list [batch|realtime]*

List the status of deployed web services.

Example Output:

+-----------+------------------------------------------+-------+----------+-----------+-------------+----------+
| NAME      | IMAGE                                    |   CPU |   MEMORY | STATUS    |   INSTANCES | HEALTH   |
|-----------+------------------------------------------+-------+----------+-----------+-------------+----------|
| mytestapp | abc.azurecr.io/mytestapp                 |   0.1 |     1024 | Running   |           1 | Healthy  |
+-----------+------------------------------------------+-------+----------+-----------+-------------+----------+


|Name|Description|
|---|---|
|Name|Name of the web service.|
|Image|Web service image location.|
|CPU|Amount of CPU used.|
|Memory|Amount of memory allocated.|
|Status|Status of the web service. The valid values are: Healthy, Scaling, Unhealthy, or Destroyed<|
|Instances|The number of instances of the web service.|
|Health|The health of the web service. |

*aml service create batch -n &lt;service name&gt; -f &lt;webservice file&gt; [-i &lt;input&gt;[=&lt;default_value&gt;] [-i &lt;input&gt;[=&lt;default_value&gt;]...]] [-o &lt;output&gt;[=&lt;default_value&gt;] [-o &lt;output&gt;[=&lt;default_value&gt;] ...]] [-p &lt;parameter&gt;[=&lt;default_value&gt;] [-p &lt;parameter&gt;[=&lt;default_value&gt;]...]] [-d &lt;dependency&gt; [-d &lt;dependency&gt;...]] [-v]*

Creates a batch web service using the specified parameters.

|Name|Required|Description|
|---|---|---|
|-n | Y | Name for the web service. |
|-f | Y | The script file containing the definition for the web service.|
|-i | N | Specifies an input variable defined in the in the web service, along with an optional default input value.|
|-o | N |Specifies an output variable defined in the in the web service, along with an optional default output location.|
|-p | N | Specifies an input parameter to the web service script file. To specify multiple parameters, use additional -p options.|
|-d | N | Specifies the path to a file on which the web the web service has a dependency. To specify multiple dependencies, use additional -d options.|
|-v | N | When specified, verbose output is provided. |


*aml service create realtime --f &lt;webservice file&gt; -n &lt;service name&gt; [-m &lt;model1&gt; [-m &lt;model2&gt;] ...] [-p requirements.txt] [-s &lt;schema&gt;] [-r spark-py|cntk-py|tensorflow-py]*


|Name|Required|Description|
|---|---|---|
|-n | Y | Name for the web service. |
|-f | Y | The script file containing the definition for the web service.|
|-m | N | The model for the web service. |
|-p | N | Specifies the path to a pip requirements.txt specifying packages to install when the web service is created. |
|-s | N |  Specifies the path to web service schema. |
|-r | N | Specifies a runtime to use for the web service. Valid values are: spark-py, cntk-py, or tensorflow-py. If you do not specify a runtime, the web service is created using the spark-py runtime. |

*aml service run batch -n &lt;service name&gt; [-j &lt;job id&gt;] [-i &lt;input&gt;=&lt;value&gt; [-i &lt;input&gt;=&lt;value&gt;...]] [-o &lt;output&gt;=&lt;value&gt; [-o &lt;output&gt;=&lt;value&gt; ...]] [-p &lt;parameter&gt;=&lt;value&gt; [-p &lt;parameter&gt;=&lt;value&gt;...]] [w]*

Starts a job on the specified batch web service.

|Name|Required|Description|
|---|---|---|
|-n | Y | The Name of the web service.|
|-j | N | An identifier for the job. |
|-i | N | Specifies input values to the web service. Inputs are defined when you use the `aml service create batch` command.|
|-o | N | Specifies the output locations for the results from the web service. |
|-p | N | Specifies input parameter values to the web service script file. |


*aml service run realtime -n service name -d input_data*

|Name|Required|Description|
|---|---|---|
|-n | Y | The Name of the web service.|
|-d | Y | Input data for the web service. The format of the data input is: '{"input":"&lt;data&gt;"}']|


*aml service view batch -n &lt;service name&gt;*

Retrieves status information about the specified batch service.

|Name|Required|Description|
|---|---|---|
|-n|Y| The Name of the web service.|

*aml service view realtime -n &lt;service name&gt;* 

Retrieves status information about the specified real-time service.

|Name|Required|Description|
|---|---|---|
|-n|Y| The Name of the web service.|

*aml service scale realtime -n &lt;service_name&gt; -c &lt;instance_count&gt;*

|Name|Required|Description|
|---|---|---|
|-n|Y| The Name of the web service.|
|-c|Y| The number of instances the web service.|


*aml service listjobs -n &lt;service name&gt;* 

Retrieves a list of jobs running against the specified web service.

|Name|Required|Description|
|---|---|---|
|-n|Y| The Name of the web service.|

*aml service viewjob -n &lt;service name&gt; -j &lt;job id&gt;* 

Retrieves status information about the specified batch job.

|Name|Required|Description|
|---|---|---|
|-n|Y| The name of the service on which the job is running.|
|-j|Y| The job ID specified when the job was started with the `aml service run batch` command.|

*aml service canceljob -n &lt;service name&gt; -j &lt;job id&gt;*

Cancels the specified batch job.

|Name|Required|Description|
|---|---|---|
|-n|Y| The name of the service on which the job is running.|
|-j|Y| The job ID specified when the job was started with the `aml service run batch` command.|


*aml service delete batch -n <service name>*

Deletes the specified batch web service.

|Name|Required|Description|
|---|---|---|
|-n|Y|The name of the web service to delete.|


*aml service delete realtime -n &lt;service name&gt;*

Deletes the specified real-time web service.

|Name|Required|Description|
|---|---|---|
|-n|Y|The name of the web service to delete.|





