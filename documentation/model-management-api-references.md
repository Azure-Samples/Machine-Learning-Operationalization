# Model Management Service API reference

For environment set-up information, see [Model Management Service getting started]().

The Model Management Service API implements the following operations:

- Register Model
- Create Manifest using a registered Model
- Create Image
- Create Service
- Delete Service
- Get Models by Hosting Account
- Get Manifests by Hosting Account
- Get Services
- Get Async Operation Status

## Register Model

Registers a model in the specified hosting account.

### Request

| Method | Request URI |
|------------|------------|
| POST       | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/hostingAccounts/{hostingAccount}/models?api-version={api\_version} |

### Properties

| Property     | Description |
|--------------------|--------------------|
| subscriptionId     | **Required**. The subscription in which the hosting account is provisioned. |
| Resource           | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccountName | **Required**. The name of the hosting account. |
| api-version        | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |

### Request Header

| Field Name     | Description |
|-----------------|----------------------|
| Content-Type    | Application/json |
| Authorization |  Bearer &lt;token> |

### Request Body

```
{
   "name": "<model name>",
   "tags": [
      <associated tag>,
      "..."
   ],
   "description": "<description content>",
   "url": "<resource url>",
   "mimeType": "<mime type of the model>",
   "unpack": "<unpack if model is zipped>"
}
```

| Field   | Description  |
|-------------|----------|
| name        | **Required**. Name of the model. Model names can contain alphanumeric characters and hyphens. Maximum length: 32 characters |
| tags        | **Optional**. Additional identifiers for a model. Tags must be alpha numeric. Maximum length: 29 characters.|
| description | **Optional**. Description of the model. If no description is provided, the default value is an empty string. Max length: 200 Unicode characters. |
| url    | **Required**. A URL specifying the location of the model. |
| mimeType    | **Optional**. The Mime type of the model. Required by Docker image generation.   |
| unpack | If the model is contained in a packaged file, specifies that is to be automatically unpackaged. For example, a zipped model resource is unzipped. Default value: False. |

### Response

The response includes an HTTP status code, a response header, and a response body.

### Status Code

-   201 - Created. Returned if the model is successfully registered.

### Response Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| x-ms-request-id | GUID. The request ID. |

### Response Body

```
{
  "id": "<model id>,
  "name": "<model name>",
  "version": "<model version>",
  "description": "<description content>",
  "url": "<resource url>",
  "tags": [
    <associated tag>,
    "..."
   ],
  "mimeType": "<mime type of the model>",
  "createdAt": "<date time of creation>"
}
```

| Field   | Description  |
|-------------|----------|
| id | A GUID that uniquely identifies the model. |
| name | Model name. Maximum length: 32 characters. |
| Tags | Additional identifiers for the model. Tags are alpha numeric. Maximum Length: 29 characters.|
| Description | *Description of the model. If no description is provided, the default value is an empty string. Max length: 200 Unicode characters. |
| url | A URL specifying the location of the model. |
| mimeType | The mime type of the model. |
| createdAt | A date/time value specifying when the model was registered. |

#----------------------------------------------------
## Create manifest

Creates a manifest using one or more models.

### Request

| Method | Request URI |
|------------|------------|
| POST       | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/hostingAccounts/{hostingAccount}/manifests?api-version={api\_version} |

### Properties

| Property     | Description                                         |
|--------------------|-------------------|
| subscriptionId     | **Required**. The subscription in which the hosting account is provisioned. |
| Resource           | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccount | **Required**. The name of the hosting account.          |
| api-version        | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |

### Request Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| Authorization| Bearer &lt;token>  |

### Request Body

```
{
   "driverProgram": "<driver program>",
   "description": "<description content>",
   "modelType": "Registered",
   "modelIds": [
      "<model Name 1>",
      "<model Name 2>",
       "...",
       "...",
       "..."
   ],
   "assets": [
      {
         "id": "<asset id>",
         "url": "<asset location url>",
         "mimeType": "<asset mime type>",
         "unPack":
      },
      ...,
      ...,
      ...
   ],
   "targetRuntime": {
      "runtimeType": "<runtime type>",
      "properties": {
         ...
      }
   }
}

```
| Field     | Description |
|---------------|---------------|
| driverProgram | **Optional**. The asset ID of the script file containing the entry point for the web service code execution. |
| description   | **Optional**. Description of the manifest. If no description is provided, the default value is an empty string. Max length: 512 Unicode characters. |
| modelType | **Required**. Must be set to 'registered'.|
| modelIds | **Required**. The list of model names. All models must reside under the same hosting account. |
| assets | **Required**. List of non-model assets that are used by the models in this manifest, including but not limited to the web service input and output schema. |
| targetRuntime | **Required**. The target runtime for the manifest. |

**asset fields**

| Field     | Description |
|---------------|---------------|
| id | **Required**. An identifier for the the asset. Identifies are are alpha numeric and can contain hyphens. Maximum Length: 32 characters |
| url | **Required**. A URL specifying the location of the asset.|
| mimetypes | **Required**. The mime-type of the asset. |
| unPack | **Required**. If the asset is contained in a packaged file, specifies that is to be automatically unpackaged. For example, a zipped model resource is unzipped. Default value: False.|


**targetRuntime fields**

| Field     | Description |
|---------------|---------------|
| runtimeType | **Required**. The runtime environment of the web service. Valid values are : parkPython, CNTKPython,  ScikitPython,  or TLC. |
| properties | **Optional**.  Additional requirements for the service. Valid property types are: *pipRequirements* and *condaEnvFile*. |

### Response

The response includes an HTTP status code, a response header, and a response body.

### Status Code

-   200 - OK. This is returned when the model successfully registered.

### Response Field Name

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| x-ms-request-id | GUID. The request ID. |

### Response Body

```
{
   "id": "<manifest id>",
   "driverProgram": "<driver program>",
   "description": "<description content>",
   "createdTime": "<time created>",
   "modelType": "<model type>",
   "modelIds": [
      "<model Name 1>",
      "<model Name 2>",
      "...",
      "...",
      "..."
   ],
   "assets": [
      {
         "id": "<asset id>",
         "url": "<asset location url>",
         "mimeType": "<asset mime type>",
         "unPack": true|false
      },
      ...,
      ...,
      ...
   ],
   "targetRuntime": {
      "runtimeType": "<runtime type>",
      "properties": {
         ...
      }
   }
}
```

| Field     | Description |
|---------------|---------------|
| id | A GUID that uniquely identifies the manifest. |
| driverProgram | The asset ID of the script file containing the entry point for the web service code execution. |
| description   | Description of the manifest. If the manifest does not have a description, an empty string is returned. Max length: 512 Unicode characters. |
| modelIds      | The list of model names included in the manifest. |
| assets        | List of non-model assets that are used by the models in this manifest. |
| targetRuntime | The target runtime for the manifest. |

**asset fields**

| Field     | Description |
|---------------|---------------|
| id | An identifier for the the asset. Identifies are are alpha numeric and can contain hyphens. Maximum Length: 32 characters  |
| url | A URL specifying the location of the asset.|
| mimetypes | The mime-type of the asset. |
| unPack | If the asset is contained in a packaged file, specifies that is to be automatically unpackaged. For example, a zipped model resource is unzipped. Default value: False. |


**targetRuntime fields**

| Field     | Description |
|---------------|---------------|
| runtimeType |  The runtime environment of the web service. Valid values are: parkPython, CNTKPython,  ScikitPython, or TLC. |
| properties | Additional requirements for the service. Valid property types are: *pipRequirements* and *condaEnvFile*.   |


#-----------------------------------------------------
## Create Image

Creates an image using the supplied manifest and image type. Currently, the only supported image type is Docker.

This is an async operation. Call the Get Async Operation Status operation with the `x-ms-request-id` to check the status of the create operation.

### Request

| Method | Request URI |
|------------|------------|
| POST       | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups /{resourceGroup}/hostingAccounts/{hostingAccount}/images?api-version={api\_version} |

### Properties

| Property     | Description                                         |
|--------------------|--------------------------|
| subscriptionId     | **Required**. The subscription in which the hosting account is provisioned. |
| Resource | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccountName | **Required**. The name of the hosting account. |
| api-version | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |

### Request Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| Authorization|   |


### Request Body

```
{
    "manifestId": "<manifest id>
    "description": "",
    "imageType": "Docker",
    "registryInfo": {
      "user": "<user name>",
      "location": "<location url>",
      "password": "<password>"
  }
}
```

| Field     | Description |
|---------------|---------------|
| manifestId | **Required**. ID of the manifest to use for image creation. |
| description | **Optional**. Description of the manifest. If no description is provided, the default value is an empty string. Max length: 512 Unicode characters. |
| imageType | **Required**. The type of image to create. Must be set to `Docker`. |
| registryInfo | **Required**. ACR Registry information. |

# registryInfo fields

| Field     | Description |
|---------------|---------------|
| user | **Required**. ACR user name. |
| location | **Required**. URL specifying the ACR location. |
| password | **Required**. ACR password. |



### Response

The response includes an HTTP status code, a response header, and a response body.

### Status Code

-   202 - Accepted

### Response Field Name

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| x-ms-request-id | GUID. The request id. |


### Response Body

Empty.

#--------------------------------------------------
## Create Service

Creates a web service based on the specified image.

This is an async operation. Call the Get Async Operation Status operation with the `x-ms-request-id` to check the status of the create operation.

### Request

| Method | Request URI |
|------------|------------|
| POST       | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups /{resourceGroup}/hostingAccounts/{hostingAccount}/services?api-version={api\_version} |

### Properties

| Property     | Description                                         |
|--------------------|---------------------------------------------------------|
| subscriptionId     | **Required**. The subscription in which the hosting account is provisioned. |
| Resource           | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccountName | **Required**. The name of the hosting account.          |
| api-version        | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |

### Request Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| Authorization | Bearer &lt;token> |


### Request Body

```
{
  "imageId": "<image id>",
  "name": "<service name>",
  "kubeConfig": "<kubeconfig string>",
  "acrImagePullSecret": "<pull secret>",
}
```

| Field     | Description |
|---------------|---------------|
| imageId | **Required**. The ID of the image to use to create the service. |
| name   | **Required**. Name of the service. |
| kubeConfig | **Required**. Kubernetes configuration information. This is the contents of your kubeconfig file. For more information, see the MMS getting started documentation. |
| acrImagePullSecret | **Required**. The name of the container registry that you have registered with kubernetes cluster. For more information, see the MMS getting started documentation. |

### Response

The response includes an HTTP status code, a response header, and a response body.

### Status Code

-   202 - Accepted

### Response Field Name

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| x-ms-request-id | GUID. The request id. |

### Response Body

Empty.

#-----------------------------------------------------------------------
## Update Service

Updates the specified web service.

This is an async operation. Call the Get Async Operation Status operation with the `x-ms-request-id` to check the status of the create operation.

### Request

| Method | Request URI |
|------------|------------|
| PUT       | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/hostingAccounts/{hostingAccount}/services/{serviceId}?api-version={api\_version}|

### Properties

| Property     | Description                                         |
|--------------------|---------------------------------------------------------|
| subscriptionId     | **Required**. The subscription in which the hosting account is provisioned. |
| resourceGroup | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccountName | **Required**. The name of the hosting account.          |
| serviceId | **Required**. The ID of the service to update. |
| api-version        | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |

### Request Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| Authorization| Bearer &lt;token>  |


### Request Body

```
{
  "manifestId": "<manifest id>",
  "acrImagePullSecret": "<pull secret>"
}
```

| Field | Description |
|-----------|-----------|
| manifestId | **Required**. The ID of the manifest to use to update the web service. |
| acrImagePullSecret| **Required**. The name of the container registry that you have registered with kubernetes cluster. For more information, see the MMS getting started documentation.|

### Response

The response includes an HTTP status code, a response header, and a response body.

### Status Code

-   202 - Accepted

### Response Field Name

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| x-ms-request-id | GUID. The request id. |

### Response Body

Empty

#-----------------------------------------------------------------------
## Delete Service

Deletes the specified service.

### Request

| Method | Request URI |
|------------|------------|
| DELETE       | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/hostingAccounts/{hostingAccount}/services/{serviceId}?api-version={api\_version} |

### Properties

| Property     | Description                                         |
|--------------------|--------------------------|
| subscriptionId | **Required**. The subscription in which the hosting account is provisioned. |
| Resource | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccountName | **Required**. The name of the hosting account.          |
| serviceId | **Required**. The ID of the service to delete. |
| api-version | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |

### Request Header

| Field Name     | Description      |
|-----------------|----------------------|
| Authorization | Bearer &lt;token> |


### Request Body

Empty.

### Response

The response includes an HTTP status code, a response header, and a response body.

### Status Code

-   200 - Ok

### Response Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| x-ms-request-id | GUID. The request id. |

### Response Body

Empty.


#--------------------------------------------------------

## Get Model Information

Gets configuration information for one or more models.

To retrieve a specific model, specify the model ID.


### Request

Retrieve a specific model.
| Method | Request URI    |
|------------|------------|
| GET        | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/hostingAccounts/{hostingAccount}/models/{id}?api-version={api\_version} |

Retrieve all models in the Hosting Account.
| Method | Request URI    |
|------------|------------|
| GET        | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/hostingAccounts/{hostingAccount}/models/?api-version={api\_version} |

### Properties

| Property     | Description                                         |
|--------------------|------------------------------|
| subscriptionId     | **Required**. The subscription in which the hosting account is provisioned. |
| resourceGroup | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccountName | **Required**. The name of the hosting account.          |
| id | ID of the model to retrieve information for. |
| api-version | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |

### Request Header

| Headers     | Description      |
|-----------------|----------------------|
| Authorization| Bearer &lt;token>  |

### Response

The response includes an HTTP status code, a response header, and a response body.

### Status Code

-   200 - OK. This is returned when the model collection could be found under this hosting account.

### Response Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| x-ms-request-id | GUID. The request id. |

### Response Body

```
[
   {
      "id": "<model id>"
      "name": "<model name>",
      "version": "<model version>",
      "description": "<description content>",
      "url": "<resource url>",
      "tags": [
         <associated tag>,
         "..."
      ],
      "mimeType": "<mime type of the model>",
      "createdAt": "<date time of creation>"
   },
   ...
]
```

| Field | Description |
|-----------|-----------|
| id | The model ID. Represented as a GUID. |
| name      | Name of the model. |
| version   | The version of the model. Versioning starts at one for the first model with the name &lt;model\_name> and increments by one for each succeeding model with the same name. |
| description | Description of the model. If no description is provided, the default value is an empty string. Max length: 200 Unicode characters. |
| url | The location of the model. |
| tags |  Additional identifiers for a model. |
| mimeType | The Mime type of the model. |
| createdAt | The date-time when this version of the model was created. |

#----------------------------------------
## Get Manifest Information

Gets information for manifests defined in the hosting account.

To retrieve a specific manifest, specify the manifest ID.

### Request

Retrieve a specific manifest.
| Method | Request URI |
|------------|------------|
| GET        | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/hostingAccounts/{hostingAccount}/manifests/{id}?api-version={api\_version} |

Retrieve all manifests in the Hosting Account
| Method | Request URI |
|------------|------------|
| GET        | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/hostingAccounts/{hostingAccount}/manifests/?api-version={api\_version} |

### Properties

| Property     | Description                                         |
|--------------------|---------------------------------------------------------|
| subscriptionId     | **Required**. The subscription in which the hosting account is provisioned. |
| resourceGroup | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccountName | **Required**. The name of the hosting account. |
| id | ID of the manifest to retrieve information for. |
| api-version | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |

### Request Header

| Field Name     | Description |
|-----------------|----------------------|
| Content-Type    | Application/json |
| Authorization |  Bearer &lt;token> |

### Response

The response includes an HTTP status code, a response header, and a response body.

### Status Code

-   200 - OK. Returned when a manifest collection is returned from the specified hosting account.

### Response Header

| Field Name | Description  |
|--------------|------------------|
| Content-Type | Application/json |

### Response Body

```
[
    {
      "id": "<manifest ID>",
      "driverProgram": "<driver program>",
      "description": "<description content>",
      "createdTime": "<date time of creation>"
      "modelIds": [
        "<model Id 1>",
        "<model Id 2>",
        "...",
        "...",
        "..."
      ],
      "assets": [
        {
          "id": "<asset id>",
          "url": "<asset location url>",
          "mimeType": "<asset mime type>",
          "unpack": "true|false"
        },
        ...,
        ...,
        ...
      ],
      "targetRuntime": {
         "runtimeType": "<runtime type>",
         "properties": {
            ...
         }
      }
    },'
    ...
]
```

| Field     | Description |
|---------------|---------------|
| id | A GUID that uniquely identifies the manifest. |
| driverProgram | he asset ID of the script file containing the entry point for the web service code execution. |
| description   | Description of the manifest. If the manifest does not have a description, an empty string is returned. Max length: 512 Unicode characters. |
| modelIds      | The list of model names included in the manifest. |
| assets        | List of non-model assets that are used by the models in this manifest. |
| targetRuntime | The target runtime for the manifest. |

**asset fields**

| Field     | Description |
|---------------|---------------|
| id | An identifier for the the asset. Identifies are are alpha numeric and can contain hyphens. Maximum Length: 32 characters  |
| url |  A URL specifying the location of the asset.|
| mimetypes | The mime-type of the asset. |
| unPack | If the asset is contained in a packaged file, specifies that is to be automatically unpackaged. For example, a zipped model resource is unzipped. Default value: False.|


**targetRuntime fields**

| Field     | Description |
|---------------|---------------|
| runtimeType |  The runtime environment of the web service. Valid values are: parkPython, CNTKPython, ScikitPython, or TLC. |
| properties | Additional requirements for the service. Valid property types are: *pipRequirements* and *condaEnvFile*.   |

#----------------------------------------------------
## Get Images

Gets a list of images associated with the specified Manifest in a Hosting Account.

To retrieve a specific image, specify the Image ID.

### Request

| Method | Request URI |
|------------|------------|
| GET       | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups /{resourceGroup}/hostingAccounts/{hostingAccount}/images/{id}?api-version={api\_version}  |

### Properties

| Property     | Description |
|--------------------|---------------------------------------------------------|
| subscriptionId | **Required**. The subscription in which the hosting account is provisioned. |
| resourceGroup | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccountName | **Required**. The name of the hosting account.          |
| id | ID of the image to retrieve information for. |
| api-version | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |

### Request Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| Authorization|   |

### Request Body

<Empty>

###  Response


### Status Code

-   200 - OK


### Response Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| x-ms-request-id | GUID. The request id.

### Response Body

```
{
   "id": "<image id>",
   "imageType": "<image type>",
   "registryInfo":{
      "user":"<user name>",
      "location":"<url of the acr>",
      "password":"<password of the acr>"
   }
}
```

| Field | Description |
|-----------|-----------|
| id | GUID. The ID of the image.|
| imageType | The type of image. Currently only Docker images are supported. |
| registryInfo | ACR Registry information. |

# registryInfo fields

| Field     | Description |
|---------------|---------------|
| user | ACR user name. |
| location | URL specifying the ACR location. |
| password | ACR password. |

#---------------------------------------------

## Get Services

Get information about services in a hosting account.

To retrieve a specific service, specify the service ID.

### Request

To retrieve a specific service.
| Method | Request URI  |
|------------|------------|
| GET        | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups /{resourceGroup}/hostingAccounts/{hostingAccount}/services/{id}?api-version={api\_version}  |

To retrieve all services in the Hosting Account.
| Method | Request URI  |
|------------|------------|
| GET        | https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups /{resourceGroup}/hostingAccounts/{hostingAccount}/services/?api-version={api\_version}  |

### Properties

| Property     | Description                                         |
|--------------------|---------------------------------------------------------|
| subscriptionId | **Required**. The subscription in which the hosting account is provisioned. |
| resourceGroup | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccountName | **Required**. The name of the hosting account.          |
| id | ID of the service to retrieve information for. |
| api-version | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |


### Request Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| Authorization|   | Bearer &lt;token> |


### Request Body

Empty.

###  Response


### Status Code

-   200 - OK


### Response Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| x-ms-request-id | GUID. The request id.

### Response Body

```
[
    {
      "id": "<service id>",
      "imageId": "<image id>",
      "name": "<service app name>",
      "createdAt": "<creation date time>",
      "updatedAt": "<last update date time>",
      "state": "<service status>",
    },
    ...
]
```

| Field | Description |
|-----------|-----------|
| id | GUID. The ID of the service.|
| imageId | GUID. The ID of the image used to create the service. |
| name | The name of the service. |
| createdAt | The date/time that the service was created. |
| updatedAt | The date/time that the service was last updated.|
| state | The state of the service. Valid values are: NotStarted, Running, Canceled, Succeeded, and Failed |

#-------------------------------------------------
## Get Async Operation Status

### Request

| Method | Request URI |
|------------|------------|
| GET       |https://eastus2euap.modelmanagement.azureml.net/api/subscriptions/{subscriptionId}/resourceGroups /{resourceGroup}/hostingAccounts/{hostingAccount}/operations/{id}?api-version={api\_version}  |

### Properties

| Property     | Description                                         |
|--------------------|---------------------------------------------------------|
| subscriptionId     | **Required**. The subscription in which the hosting account is provisioned. |
| resourceGroup | **Required**. The name of the resource group in which the hosting account is provisioned. |
| hostingAccountName | **Required**. The name of the hosting account.          |
| id | ID of the operation to retrieve information for. |
| api-version | **Required**. Version of the API to be used with the request. The current version is `2017-06-01-privatepreview`. |

### Request Header

| Field Name     | Description      |
|-----------------|----------------------|
| Authorization| Bearer &lt;token>  |

### Request Body

Empty.

### Response

### Status Code

- 200 - OK

### Response Header

| Field Name     | Description      |
|-----------------|----------------------|
| Content-Type    | Application/json     |
| x-ms-request-id | GUID. The request id. |

### Response Body

```
{
  "id": "<operation id>",
  "operationType": "<Image|Service>",
  "resourceLocation": "<url to get the created resource>",
  "createdTime": "<creation date time>",
  "endTime": "<end date time>",
  "state": "<NotStarted|Running|Cancelled|Succeeded|Failed>",
  "error": {
    <error response detail>
  }
}
```

| Field | Description |
|-----------|-----------|
| id | GUID. The ID of the operation for which information is being returned.|
| operationType | Specifies the type of operation for which information is being returned.  |
| resourceLocation |  |
| endTime |  |
| state | The state of the operation being checked. Valid values are:  <NotStarted|Running|Canceled|Succeeded|Failed>|
| error | An error object that contains information about error conditions on the operation being checked. |