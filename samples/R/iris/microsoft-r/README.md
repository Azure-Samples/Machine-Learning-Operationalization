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

# import bundleService
source('https://raw.githubusercontent.com/danhartl/Machine-Learning-Operationalization/master/utils/BundleService.R')

library(RevoScaleR);

# train model

trainData <- iris; formula <- Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width;
irisModel <- rxBTrees(formula, data = trainData, lossFunction = 'multinomial', nTree = 3,learningRate = 0.1, sampRate = 0.5, maxdepth = 1, minBucket = 1,seed = 1234, replace = FALSE, mTry = 0, maxNumBins = 200);

# define operationalization functions

init <- function() {
  library(RevoScaleR)
}

predictIris <- function(SepalLength, SepalWidth, PetalLength, PetalWidth) {
  input <- data.frame(Sepal.Length = c(SepalLength), Sepal.Width = c(SepalWidth), Petal.Length = c(PetalLength), Petal.Width = c(PetalWidth))
  
  prediction <- rxPredict(model, data = input)
  result <<- as.character(prediction$Species_Pred)
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

```csharp
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