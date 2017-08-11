Model Management Service (preview) provides programmatic management of your Azure Machine Learning models, manifests, and images.

## Common parameters and header fields

All of the MMS API REST operations conform to the HTTP/1.1 protocol specification and each operation returns an x-ms-request-id response header that can be used to obtain information about the request. You must also make sure that requests made to these resources are secure. 

- Replace {subscriptionId} in the request URI with your subscription identifier.
resourceGroup
- Replace {resourceGroup} in the request URI with the Resource Group in which your Hosting Account exists.
- Replace {hostingAccount} in the request URI with your Hosting Account.
- Replace {api-version} with .
- Set the Content-Type request header to application/json.
- Set the Authorization request header to an OAuth bearer token formatted as a JSON Web Token, which you obtain from Azure Active Directory. For more information, see Azure REST API Reference.

## Setup

Before you call the MMS API, you must set up your Azure Machine Learning operationalization environment.

For set up information, see [Operationalizing ML Models on Azure (Preview)](https://github.com/Azure/Machine-Learning-Operationalization/blob/master/documentation/getting-started.md) .

The *Create Service* operation requires that you supply Kubernetes configuration information for the call.

The *kubeconfig* file is located in the .kube folder. 

- On linux:  ~/.kube/config
- On Windows: c:\users\\\<user name>\\.kube

If you do not find the kubeconfig file, you can retrieve it by running the following command: 

```
az acs kubernetes get-credentials --resource-group=<resource group name> --name=<kubernetes cluster name>
```

Before passing the file in the payload for the *Create Service* operation, remove new lines from the file. From bash a bash shell, you can use the following command to remove new lines:

```
tr -d "\n\r" < config
```
You must supply an ACR image pull secret when calling the following operations:

- *Create Service*
- *Update Service*

To create an ACR image pull secret, run the following command:

```
kubectl create secret docker-registry <registry key name> --docker-server=<Docker server URL> --docker-username=<user name> --docker-password=<password> --docker-email=<email address>
```
## How to use the MMS API to deploy a web service

1. Set up your environment
    1. Get kubeconfig
    2. Create ACR image pull secret
2. Create Hosting Account
3. Register a Model in the Hosting account
4. Create a Manifest based on the model
5. Create an Image based on the manifest
    1. Call the *Operation Status* operation to poll to determine when the Image is successfully created
    2. Retrieve the Image ID 
6. Create the web service based on the Image
    1. Call the *Operation Status* operation to poll to determine when the Web Service is successfully created