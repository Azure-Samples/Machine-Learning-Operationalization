
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml import Pipeline, PipelineModel
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.sql import Row
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import *
import argparse

sc = SparkContext.getOrCreate()
sqlContext = SQLContext.getOrCreate(sc)
sc._jsc.hadoopConfiguration().set('fs.azure.account.key.<acct>.blob.core.windows.net','<acctKey>')

parser = argparse.ArgumentParser()
parser.add_argument("--input-data")
parser.add_argument("--trained-model")
parser.add_argument("--output-data")

args = parser.parse_args()
print str(args.input_data)
print str(args.trained_model)
print str(args.output_data)

def csvParse(s):
    import csv
    from StringIO import StringIO
    sio = StringIO(s)
    value = csv.reader(sio).next()
    sio.close()
    return value

model = PipelineModel.load(args.trained_model)

testData = sc.textFile(str(args.input_data))\
             .map(csvParse) \
             .map(lambda l: (int(l[0]), l[1], l[12], l[13]))

schema = StructType([StructField("id", IntegerType(), False), 
                     StructField("name", StringType(), False), 
                     StructField("results", StringType(), False), 
                     StructField("violations", StringType(), True)])

testDf = sqlContext.createDataFrame(testData, schema).where("results = 'Fail' OR results = 'Pass' OR results = 'Pass w/ Conditions'")

predictionsDf = model.transform(testDf)

predictionsDf.write.mode('overwrite').parquet(str(args.output_data))
