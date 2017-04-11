from tensorflow.examples.tutorials.mnist import input_data
import json
import numpy
import requests
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--imgIdx", type=str, help="Index of the image from the MNIST dataset to use as input.", required=True)
parser.add_argument("--url", type=str, help="URL for the prediction service", required=True)
parser.add_argument("--name", type=str, help="name of the prediction service", required=True)
args = parser.parse_args()

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)
input_data = numpy.array([mnist.test.images[int(args.imgIdx)]])
input_data_string = json.dumps(input_data.tolist())
data = json.dumps({"input":input_data_string})
routing_id = "/{0}".format(args.name)
headers = {'Content-Type':'application/json', 'X-Marathon-App-Id': routing_id}
print(headers)

result = requests.post(args.url,headers=headers,data=data)
print(result.text)
number = json.loads(result.content.decode('ascii'))
print(number['result'])
