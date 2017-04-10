import numpy as np
import logging, sys, json
import timeit as t
import urllib.request
import base64
from cntk.ops.functions import load_model
from PIL import Image
from io import BytesIO

logger = logging.getLogger("cntk_svc_logger")
ch=logging.StreamHandler(sys.stdout)
logger.addHandler(ch)

trainedModel=None
mem_after_init=None
labelLookup = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
imageMean = 133.0
topResult = 3

def aml_cli_get_sample_request():
    return 'Sample request here'

def init():
  global trainedModel, mem_after_init

  start = t.default_timer()
  # Load the model from disk and perform evals
  trainedModel = load_model('resnet.dnn')
  end = t.default_timer()

  loadTimeMsg = "Model loading time: {0} ms".format(round((end-start)*1000, 2))
  logger.info(loadTimeMsg)

def run(inputString):

  start = t.default_timer()
  
  images=json.loads(inputString)
  result = []
  totalPreprocessTime = 0
  totalEvalTime = 0
  totalResultPrepTime = 0
  
  for base64ImgString in images:

    if base64ImgString.startswith('b\''):
      base64ImgString = base64ImgString[2:-1]
    base64Img = base64ImgString.encode('utf-8')
    
    # Preprocess the input data 
    startPreprocess = t.default_timer()
    decoded_img = base64.b64decode(base64Img)
    img_buffer = BytesIO(decoded_img)
    imageData = np.array(Image.open(img_buffer), dtype=np.float32)
    imageData -= imageMean
    imageData = np.ascontiguousarray(np.transpose(imageData, (2, 0, 1)))
    endPreprocess = t.default_timer()
    totalPreprocessTime += endPreprocess - startPreprocess

    # Evaluate the model using the input data
    startEval = t.default_timer()
    imgPredictions = np.squeeze(trainedModel.eval({trainedModel.arguments[0]:[imageData]}))
    endEval = t.default_timer()
    totalEvalTime += endEval - startEval

    # Only return top 3 predictions
    startResultPrep = t.default_timer()
    resultIndices = (-np.array(imgPredictions)).argsort()[:topResult]
    imgTopPredictions = []
    for i in range(topResult):
      imgTopPredictions.append((labelLookup[resultIndices[i]], imgPredictions[resultIndices[i]] * 100))
    endResultPrep = t.default_timer()
    result.append(imgTopPredictions)

    totalResultPrepTime += endResultPrep - startResultPrep

  end = t.default_timer()

  logger.info("Predictions: {0}".format(result))
  logger.info("Predictions took {0} ms".format(round((end-start)*1000, 2)))
  logger.info("Time distribution: preprocess={0} ms, eval={1} ms, resultPrep = {2} ms".format(round(totalPreprocessTime * 1000, 2), round(totalEvalTime * 1000, 2), round(totalResultPrepTime * 1000, 2)))
  
  actualWorkTime = round((totalPreprocessTime + totalEvalTime + totalResultPrepTime)*1000, 2)
  return (result, 'Computed in {0} ms'.format(actualWorkTime))
