# Operationalizing R Models in AzureML

## Create Bundle

```R
source('https://raw.githubusercontent.com/danhartl/Machine-Learning-Operationalization/master/utils/BundleService.R')

init <- function() {
  d <<- 3
}

add <- function(x, y) {
  result <<- (x + y) * myModel + d
}

bundleService(init, add, list(myModel = 2), inputs = list(x = "numeric", y = "numeric"), outputs = list(result = "numeric"), "/tmp")
```

## Deploy

```
az ml service create realtime -n myservice1 -r mrs -f service.json -d init -d run -d myModel
```

## Test

```
az ml service run realtime -n myservice1 -d '{"x" : 2, "y": 3}
```