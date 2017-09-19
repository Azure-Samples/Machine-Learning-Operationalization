import requests
import json

data = "{\"doc_text\": \"OpenGL on the GPU is fast\"}"
body = str.encode(json.dumps(data))

url = 'http://127.0.0.1:32769/score' 
api_key = 'your service key'  
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)} 

resp = requests.post(url, data, headers=headers)
print(resp.text)
