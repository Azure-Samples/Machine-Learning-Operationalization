# Operationalization and Model Management Command Line Interface Reference

You can update your Azure ML CLI installation using pip. To perform the update, you must have sufficient permissions: 

**Linux**: On Linux you must be running as sudo:

```
$ sudo -i
```

Then issue the following command:
```
# wget -q https://raw.githubusercontent.com/Azure/Machine-Learning-Operationalization/master/scripts/amlupdate.sh -O - | sudo bash -
```

**Windows**: On Windows, you must run the command as administrator.

Then issue the following command:

```
pip install azure-cli-ml
```

## Base CLI concepts:

    account : Manage model management accounts.	
    env     : Manage compute environments.
    image   : Manage operationalization images.
    manifest: Manage operationalization manifests.
    model   : Manage operationalization models.
    service : Manage operationalized services.

## Account commands
A model management account is required to use the services which allow you to deploy and manage models.

    create: Create a Model Management Account.
    delete: Delete a specified Model Management Account.
    list  : Gets the Model Management Accounts in the current subscriptiong.
    set   : Set the active Model Management Account.
    show  : Show a Model Management Account.
    update: Update an existing Model Management Account.

**Create Model Managment Account**

Create a model managment account using the below command. This account will be used for billing.

*az ml account modelmanagement create --location [Azure region e.g. eastus2] --name [your new account name] --resource-group [resource group name to store the account in] --sku-capacity 1 --sku-name S1*

Local Arguments:


    --location -l       [Required]: Resource location.
    --name -n           [Required]: Name of the model management account.
    --resource-group -g [Required]: Resource group to create the model management account in.
    --sku-capacity      [Required]: Sku capacity. Used to scale the max capacity for resources
                                    managed by this account. Must be between 1 and 16 inclusive.
    --sku-name          [Required]: Sku name. Valid names are S1|S2|S3|DevTest.
    --description -d              : Description of the model management account.
    --tags -t                     : Tags for the model management account.  Default: {}.
    -v                            : Verbosity flag.


## Environment commands

    delete         : Delete an MLCRP-provisioned resource.
    get-credentials: Gets the credentials for the specified cluster such as Storage, ACR and ACS
                     credentials.
    list           : Gets the operationalization clusters in the specified subscription.
    local          : Switch to local mode.
    set            : Set the active MLC environment.
    setup          : Sets up an MLC environment.
    show           : Show an MLC resource; If resource_group or cluster_name are not provided, shows
                     the active MLC env.

**Set up the Deployment Environment**

There are two option for deployment: local or cluster. 

*az ml env setup [-c][-l] --name[your-cluster-name]*

Initializes your Azure machine learning environment with a storage account, ACR registry, App Insights service, and an ACS cluster created in your subscription. By default, the environment is initialized for local deployments only (no ACS) if no flag is specified. If you need to scale service, you can specify -c flag to create an ACS cluster.

Command details:

    --cluster-name -n    [Required]: Name of cluster to provision.
    --agent-count -z               : Number of agents to provision for the cluster.  Default: 2.
    --cluster -c                   : Flag to provision ACS cluster. Defaults to false.
    --location -l                  : Location to provision ACS cluster. Required if provisioning in
                                     cluster mode. Ignored if provisioning in local mode.
    --resource-group -g            : Resource group in which to create compute resource. Will be
                                     created if it does not exist. If not provided, resource group
                                     will be created with 'rg' appended to 'name.'.
    --service-principal-app-id -a  : App ID of service principal to use for configuring ML compute.
    --service-principal-password -p: Password associated with service principal.
    --yes -y                       : Flag to answer 'yes' to any prompts. Command will fail if user
                                     is not logged in.

**Local mode**

*az ml env local*

In local mode, the CLI creates locally running web services for development
and testing. To run the CLI in local mode, set the following environment variables:

| Variable | Description |
|---|---|
| AML_STORAGE_ACCT_NAME | Set this to an Azure storage account. For more information about Azure storage accounts, see https://docs.microsoft.com/en-us/azure/storage/storage-introduction |
| AML_STORAGE_ACCT_KEY | Set this to either the primary or secondary key of the preceding storage account. |
| AML_ACR_HOME | The URL of your Azure Container Registry (ACR). For more information about the Azure Container Registry, see https://docs.microsoft.com/en-us/azure/container-registry/container-registry-intro |
| AML_ACR_USER | The username of the ACR specified by AML_ACR_HOME. |
| AML_ACR_PW  | The password of the ACR specified by AML_ACR_HOME. |
| AML_APP_INSIGHTS_NAME | Set this to an App Insights account. |
| AML_APP_INSIGHTS_KEY  | The App Insights instrumentation key. |

**Cluster mode**

In the cluster mode, the model is deployed to and runs on the ACS cluster which is set up using the env setup command above. To use the environment you have set up before, use the following command.

*az ml env set --cluster-name [your cluster name used in env setup call] -g [resrouce group name]*

In cluster mode, the CLI is used to deploy production web services using ACS with Kubernetes. For more information on ACS, see https://docs.microsoft.com/en-us/azure/container-service/container-service-intro.

**Switching to local**

*az ml env local*

Switches to the local deployment environment. 

## Image commands

    create: Create an Operationalization Image. This command has two different sets of
            required arguments, depending on if you want to use a previously created manifest.
    list: List images created
    show: Show image details for an image

**Create image**

Note that the create service command listed below can perform the create image operation. So you don't have to create an image separately. 

You can create an image with the option of having registered it before, or register it with a single command (shown below).

*az ml image create -n [image name] --model-file [model file or folder path] -f [code file e.g. the score.py file] -r [the runtime eg.g. scikit-pay which is the Docker container image base]*

Command details:

    --image-name -n [Required]: The name of the image being created.
    --image-description       : Description of the image.
    --image-type              : The image type to create. Defaults to "Docker".  Default: Docker.
    -v                        : Verbosity flag.

Registered image:

    --manifest-id             : [Required] Id of previously registered manifest to use in image
                                creation.
Unregistered image:

    --dependency -d           : Files and directories required by the service. Multiple dependencies
                                can be specified with additional -d arguments.
    --model-file -m           : [Required] Model file to register.
    --schema-file -s          : Schema file to add to the manifest.
    -f                        : [Required] The code file to be deployed.
    -p                        : A pip requirements.txt file needed by the code file.
    -r                        : [Required] Runtime of the web service. Valid runtimes are spark-
                                py|cntk-py|tlc|scikit-py.

## Manifest commands

    create: Create an Operationalization Manifest. This command has two different
            sets of required arguments, depending on if you want to use previously registered
            model/s.
    list: List of manifests
    show: Show manifest details

**Create manifest**

Creates a manifest file for the model. Note that you can use the service create command which will perform the manifest creation (without you having to create it separately).

*az ml manifest create --manifest-name [your new manifest name] -f [path to code file] -r [runtime for the image e.g. scikit-py]*


Command details:

    --manifest-name -n [Required]: Name of the manifest to create.
    -f                 [Required]: The code file to be deployed.
    -r                 [Required]: Runtime of the web service. Valid runtimes are spark-py|cntk-
                                   py|tlc|scikit-py.
    --dependency -d              : Files and directories required by the service. Multiple
                                   dependencies can be specified with additional -d arguments.
    --manifest-description       : Description of the manifest.
    --schema-file -s             : Schema file to add to the manifest.
    -p                           : A pip requirements.txt file needed by the code file.
    -v                           : Verbosity flag.

## Model commands

    list: List created models
    register: Register the model
    show: Show model details

**Register a model**

Command to register the model. Note that you can use the service create command which will perform the model registraiton (without you having to register it separately).

*az ml model register --model [path to model file] --name [model name]*

Command details:

    --model -m [Required]: Model to register.
    --name -n  [Required]: Name of model to register.
    --description -d     : Description of the model.
    --tag -t             : Tags for the model. Multiple tags can be specified with additional -t
                           arguments.
    -v                   : Verbosity flag.

## Service commands

    create
    delete
    keys
    list
    run
    scale
    show
    update

**Create a service**

In the below command, note that the schema needs to be generate-schema command available through the Azure ML SDK (see samples for more info on the schema creation). 

*az ml service create realtime --model-file [path to model file(s)] -f [path to model scoring file e.g. score.py] -n [your service name] -s [schema file e.g. service_schema.json] -r [run time included in the image e.g. spark-py]*

Commands details:

    --conda-file -c     : Path to Conda Environment file.
    --image-type        : The image type to create. Defaults to "Docker".  Default: Docker.
    --model-file -m     : [Required] The model to be deployed.
    -d                  : Files and directories required by the service. Multiple dependencies can
                          be specified with additional -d arguments. 
    -f                  : [Required] The code file to be deployed.
    -p                  : A pip requirements.txt file of package needed by the code file.
    -r                  : [Required] Runtime of the web service. Valid runtimes are spark-py|cntk-
                          py|tlc|scikit-py.
    -s                  : Input and output schema of the web service.

Note on the -d flag for attaching dependencies: If you pass the name of a directory that is not already bundled (zip, tar, etc.) that directory automatically gets tar’ed, and is passed along, then automatically un-bundled on the other end. If you pass in a directory that is already bundled we treat it as a file and pass it along as is. It will not be un-bundled automatically, and you would be expected to handle that in your code.

**Get service details**

Get service details including URL, usage (including sample data if a schema was created).

*az ml service show realtime --name [your service name]*

Command details:

    --id -i    : The service id to show.
    --name -n  : The service name.
    -v         : Verbosity flag.

**Run the service**

*az ml service run realtime -n [service name] -d [input_data]*

Command details:

    --id -i    : The MMS service id to score against.
    --name -n  : Webservice name.
    -d         : The data to use for calling the web service.
    -v         : Verbosity flag.


**Scale the service**

*az ml service scale realtime -n [service name] -z [number of replicas]*

Command details:

    -n [Required]: Webservice name.
    -z [Required]: Number of replicas for a Kubernetes service.  Default: 1.




