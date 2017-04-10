import base64, requests, json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--img", type=str, help="Local path to the 32x32 image to use for prediction", required=True)
parser.add_argument("--url", type=str, help="URL for the prediction service", required=True)
parser.add_argument("--name", type=str, help="name of the prediction service", required=True)
args = parser.parse_args()

routing_id="/{0}".format(args.name)
headers = {'Content-Type': 'application/json', 'X-Marathon-App-Id': routing_id}
#print(headers)
encoded = None
with open(args.img, 'rb') as file:
  encoded = base64.b64encode(file.read())
payload = {
      'input': '["{0}"]'.format(encoded)
}
body = json.dumps(payload)

r = requests.post(args.url, data = body, headers=headers)
print(r.text)

