import uuid
import random
import time
import requests
import json

endpoint = 'http://localhost:5000/api/vote'

# for i in range(1008):
#     time.sleep(0.2)
#     vote = {
#         'data': {
#             'voter_id': str(uuid.uuid4()),
#             'campaign_id': 1,
#             'candidate_id': random.randint(1, 4),
#             'timestamp': str(time.time())
#         }
#     }
#     x = requests.post(endpoint, json=json.dumps(vote))

for i in range(504):
    time.sleep(0.2)
    vote = {
        'data': {
            'voter_id': str(uuid.uuid4()),
            'campaign_id': 2,
            'candidate_id': random.randint(1, 3),
            'timestamp': str(time.time())
        }
    }
    x = requests.post(endpoint, json=json.dumps(vote))
