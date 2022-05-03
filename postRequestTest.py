import requests
import json



webhook_url = 'http://87.59.207.21:8000/webhook'

data = {
    "test":"test" }

r = requests.post(webhook_url,data=json.dumps(data), headers={'Content-Type': 'application/json'})

print(r)