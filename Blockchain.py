from collections import deque
from helpers import hash_vote
import uuid
import time
import json
from block import Block
import redis
from file_manager import FileManager

# Class used for managing shards.
class Blockchain:
    def __init__(self, file_manager):
        self.file_manager = file_manager
        # Configure redis client for connecting with the cache.
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_client = redis_client
        self.stats = []

    # Checks if a user has voting by loading every shard and checking if the user exists. 
    # Adds entry to cache to improve performance of future accesses.
    def has_voted(self, voter_id, campaign_id):
        cache_result = self.redis_client.get(f"{voter_id}_{campaign_id}")
        if cache_result is not None:
            return True
        shard_count = self.file_manager.get_shard_count()
        for i in range(shard_count):
            shard = self.file_manager.get_shard(i)
            if shard.has_voted(voter_id, campaign_id):
                self.redis_client.set(f"{voter_id}_{campaign_id}", str(True))
                return True
        return False

    # Returns statistics of entire blockchain by getting the stats for each individual shard.
    def get_stats(self):
        shard_count = self.file_manager.get_shard_count()
        if shard_count == 0:
            return {}
        stats = {}
        for i in range(0, shard_count):
            shard = self.file_manager.get_shard(i).shard
            for j in range(len(shard)):
                block = shard[j]
                for vote_info in block.votes:
                    campaign_id = vote_info['campaign_id']
                    candidate_id = vote_info['candidate_id']
                    if campaign_id not in stats:
                        stats[campaign_id] = {}
                    stats[campaign_id][candidate_id] = stats[campaign_id].get(
                        candidate_id, 0) + 1
        return stats


if __name__ == "__main__":
    file_manager = FileManager(5000)
    blockchain = Blockchain(file_manager)
    print(blockchain.get_stats())
