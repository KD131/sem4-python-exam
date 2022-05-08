import requests
import json



webhook_url = 'http://elcaptaino.duckdns.org:8000/webhook'

data = {
    "test":"test" }

r = requests.post(webhook_url,data=json.dumps(data), headers={'Content-Type': 'application/json'})

print(r)