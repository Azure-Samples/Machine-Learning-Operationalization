import requests
import json

data = "{\"doc_text\": \"OpenGL on the GPU is fast\"}"
body = str.encode(json.dumps(data))

url = 'http://127.0.0.1:32769/score' 
headers = {'Content-Type':'application/json'}

resp = requests.post(url, data, headers=headers)
print(resp.text)