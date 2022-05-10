import requests
import json
import uuid 



webhook_url = 'http://elcaptaino.duckdns.org/webhook'
test_url = 'http://172.18.0.3:8000/webhook'

data = {'message': {'data': 'eyJlbWFpbEFkZHJlc3MiOiJweXRob25kaWxsZXJAZ21haWwuY29tIiwiaGlzdG9yeUlkIjoyMzk4fQ==', 'messageId': '4584729288918052', 'message_id': '4584729288918052', 'publishTime': '2022-05-10T08:22:02.877Z', 'publish_time': '2022-05-10T08:22:02.877Z'}, 'subscription': 'projects/exam-project-349112/subscriptions/exam-project-349112-topic-sub'}

r = requests.post(test_url,data=json.dumps(data), headers={'Content-Type': 'application/json'})

print(r)
