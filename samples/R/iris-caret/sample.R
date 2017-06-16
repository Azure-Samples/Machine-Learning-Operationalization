# import bundleService
source('https://raw.githubusercontent.com/danhartl/Machine-Learning-Operationalization/master/utils/BundleService.R')



library(caret)
data(iris)
set.seed(12345)
inTrain<-createDataPartition(iris$Species,p=0.7,list=FALSE)
training<-iris[inTrain,]
testing<-iris[-inTrain,]

irisModel<-train(Species~.,method="rpart",data=iris)

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
  outputFolder = "d:\\temp\\service3")
