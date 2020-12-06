import hashlib
from collections import OrderedDict
from hashlib import sha256
import json
import time
import uuid
from helpers import GENESIS_BLOCK_VALUES, hash_vote


class MerkleTreeBlock:
    def __init__(self, prev_hash, timestamp, votes):
        self.prev_hash = prev_hash
        self.timestamp = timestamp
        self.votes = votes
        hashes = []
        for vote in votes:
            hashes.append(self.hash_vote(vote))
        votes_root_hash = self.get_votes_hash(hashes)
        self.merkle_root_hash = self.get_root_hash(
            prev_hash, timestamp, votes_root_hash)

    @staticmethod
    def create(prev_block, votes):
        timestamp = str(time.time())
        return MerkleTreeBlock(prev_block.merkle_root_hash, timestamp, votes)

    @staticmethod
    def genesis_block():
        # Initialize genesis block with dummy values.
        return MerkleTreeBlock(GENESIS_BLOCK_VALUES['prev_hash'], GENESIS_BLOCK_VALUES['timestamp'], GENESIS_BLOCK_VALUES['votes'])

    def get_root_hash(self, prev_hash, timestamp, votes_hash):
        combined_hash = timestamp + prev_hash + votes_hash
        return sha256(combined_hash.encode()).hexdigest()

    def hash_vote(self, vote_info):
        sorted_keys = sorted(list(vote_info.keys()))
        sorted_tuples = [(key, vote_info[key]) for key in sorted_keys]
        ordered_dict = OrderedDict(sorted_tuples)
        vote_info_json_string = json.dumps(ordered_dict)
        return sha256(vote_info_json_string.encode()).hexdigest()

    def get_votes_hash(self, hashes):
        sorted_hashes = sorted(hashes)
        if len(sorted_hashes) % 2 != 0:
            sorted_hashes.append(sorted_hashes[-1:][0])

        combined = []
        for i in range(0, len(sorted_hashes), 2):
            first = sorted_hashes[i]
            second = sorted_hashes[i + 1]
            combined_hash = sha256((first + second).encode()).hexdigest()
            combined.append(combined_hash)

        if len(combined) == 1:
            return combined[0]
        else:
            return self.get_votes_hash(combined)


if __name__ == '__main__':
    block = MerkleTreeBlock("hash", "123", [
        {
            'voter_id': 1,
            'campaign_id': 1,
            'candidate_id': 3,
            'timestamp': 3
        },
        {
            'voter_id': 2,
            'campaign_id': 1,
            'candidate_id': 2,
            'timestamp': 4
        },
        {
            'voter_id': 3,
            'campaign_id': 1,
            'candidate_id': 1,
            'timestamp': 5
        }
    ])

    print(MerkleTreeBlock.create(block, [
        {
            'voter_id': 1,
            'campaign_id': 1,
            'candidate_id': 3,
            'timestamp': 3
        },
        {
            'voter_id': 3,
            'campaign_id': 1,
            'candidate_id': 2,
            'timestamp': 4
        },
        {
            'voter_id': 6,
            'campaign_id': 1,
            'candidate_id': 1,
            'timestamp': 5
        },
        {
            'voter_id': 7,
            'campaign_id': 1,
            'candidate_id': 1,
            'timestamp': 5
        },
    ]).merkle_root_hash)

    # print("root hash", block.merkle_root_hash)
