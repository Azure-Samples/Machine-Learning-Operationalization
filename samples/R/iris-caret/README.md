# Operationalizing R Models in AzureML

## Setup

Create AzureML cluster

```
az ml env setup -k
```

## Create Bundle

```R
# import bundleService
source('https://raw.githubusercontent.com/danhartl/Machine-Learning-Operationalization/master/utils/BundleService.R')

library(caret)
data(iris)
set.seed(12345)
inTrain<-createDataPartition(iris$Species,p=0.7,list=FALSE)
training<-iris[inTrain,]
testing<-iris[-inTrain,]

# train model

irisModel<-train(Species~.,method="rpart",data=iris)

# define operationalization functions

init <- function() {
  library(caret)
}

predictIris <- function(SepalLength, SepalWidth, PetalLength, PetalWidth) {
  input <- data.frame(Sepal.Length = c(SepalLength), Sepal.Width = c(SepalWidth), Petal.Length = c(PetalLength), Petal.Width = c(PetalWidth))
  result <<- as.character(predict(model, input))
}

bundleService(
  init,
  predictIris,
  list(model = irisModel),
  inputs = list(SepalLength = "numeric", SepalWidth = "numeric", PetalLength = "numeric", PetalWidth = "numeric"),
  outputs = list(result = "character"),
  outputFolder = "/tmp")

```

## Deploy

```
az ml service create realtime -n myservice1 -r mrs -f service.json -d init -d run -d model
```

## Test

```
az ml service run realtime -n myservice1 -d '{ "SepalLength": 4.7, "SepalWidth": 3.2, "PetalLength": 1.3, "PetalWidth": 0.2 }'
```

## Generate client code

You can download the swagger.json metadata from /swagger.json

Store it in a file and you can use [autorest](https://www.nuget.org/packages/AutoRest) to generate the client code:

```
.\AutoRest.exe -input 'swagger.json' -ClientName Service -CodeGenerator CSharp -Namespace 'AzureML' -OutputDirectory '/tmp'
```

With this you can create a sample C# application

```
internal class Program
{
    private static void Main(string[] args)
    {
        var service = new Service(new Uri("<servername>"));

        var webServiceResult = service.RunMLService(new InputParameters(4.7, 3.2, 1.3, 0.2));
        Console.WriteLine(webServiceResult.OutputParameters.Result);
    }
}
```