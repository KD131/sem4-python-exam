import requests
import json
import uuid 



webhook_url = 'http://elcaptaino.duckdns.org/webhook'

data = {
    "test":"test" }

r = requests.post(webhook_url,data=json.dumps(data), headers={'Content-Type': 'application/json'})

print(r)
