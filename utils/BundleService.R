library(jsonlite)

bundleService <- function(init, run, objects, inputs, outputs, folder)
{
  saveToFile <- function(name, obj) {
    binFile <- file(paste(folder, '/', name, sep = ''), 'wb')
    binObj <- serialize(obj, NULL)
    writeBin(con = binFile, object = binObj)
    close(binFile)
  }
  
  saveToFile('init', init)
  saveToFile('run', run)

  preloadedObjects <- list(unbox('init'), unbox('run'))
  
  mapply(function(value, name) {
    assign(name,value)
    saveToFile(name, value)
  }, objects, names(objects))

  for(objName in names(objects)) {
    preloadedObjects[[length(preloadedObjects)+1]] <- unbox(objName)
  }
  
  argumentList = ''
  
  for(arg in names(inputs)) {
    if(argumentList != '') {
      argumentList = paste(argumentList, ', ', sep = '')
    }
  
    argumentList = paste(argumentList, arg, sep = '')
  }
  
  convertToParameterDefinition <- function(parameters) {
    result <- list()
  
    for(key in names(parameters)) {
      result[[length(result)+1]] <- structure(list(name=unbox(key), type=unbox(parameters[[key]])))
    }
    
    result
  }
  
  svcmetadata <- structure(list(
    runtimeType = unbox("R"),
    initCode = unbox("init()"),
    code = unbox(paste("run(", argumentList, ")", sep = '')),
    inputParameterDefinitions = convertToParameterDefinition(inputs),
    outputParameterDefinitions = convertToParameterDefinition(outputs),
    preloadedObjects = preloadedObjects
  ))

  json <- toJSON(svcmetadata, pretty=TRUE)
  write(json, paste(folder, '/service.json', sep = ''))
}