from locust import HttpUser, task, between
import uuid
import time
import json


class WebsiteTestUser(HttpUser):
    # Tests voting endpoint through simulated users and requests.
    @task(1)
    def vote(self):
        self.client.post("http://localhost:5000/api/vote", json={"data": {"voter_id": str(
            uuid.uuid4()), "campaign_id": 2, "candidate_id": 4, "timestamp": str(time.time())}})

    # Tests initial shard retrieval.
    @task(2)
    def get_votes(self):
        self.client.get("http://localhost:5000/api/get_votes/0")
