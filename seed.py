import uuid
import random
import time
import requests
import json

endpoint = 'http://localhost:5000/api/vote'

def make_request(vote):
    try:
        requests.post(endpoint, json=json.dumps(vote))
    except:
        print("Failed to send vote info for campaign 1")


if __name__ == "__main__":
    for i in range(1, 10000):
        if i % 100 == 0:
            print(i)

        time.sleep(0.1)
        make_request({
            'data': {
                'voter_id': str(uuid.uuid4()),
                'campaign_id': 1,
                'candidate_id': random.randint(1, 4),
                'timestamp': str(time.time())
            }
        })

        time.sleep(0.1)
        make_request({
            'data': {
                'voter_id': str(uuid.uuid4()),
                'campaign_id': 2,
                'candidate_id': random.randint(1, 3),
                'timestamp': str(time.time())
            }
        })

