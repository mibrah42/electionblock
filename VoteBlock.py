import time
import uuid
import math
import binascii
from helpers import GENESIS_BLOCK_VALUES, hash_vote


class VoteBlock:
    def __init__(self, prev_hash, hash, timestamp, vote_info):
        self.prev_hash = prev_hash
        self.hash = hash
        self.timestamp = timestamp
        self.vote_info = vote_info

    @staticmethod
    def genesis_block():
        # Initialize genesis block with dummy values.
        return VoteBlock(GENESIS_BLOCK_VALUES['prev_hash'], GENESIS_BLOCK_VALUES['hash'], GENESIS_BLOCK_VALUES['timestamp'], GENESIS_BLOCK_VALUES['vote_info'])

    @staticmethod
    def create(prev_block, vote_info):
        current_time = str(time.time())
        new_hash = hash_vote(prev_block.hash, current_time, vote_info)

        return VoteBlock(prev_block.hash, new_hash, current_time, vote_info)


if __name__ == "__main__":
    block = VoteBlock('prev_hash', 'hash', str(time.time()), {
        'voter_id': str(uuid.uuid4()),
        'campaign_id': 1,
        'candidate_id': 2,
        'timestamp': str(time.time())
    })

    print(block.__dict__)

    print(VoteBlock.create(block, {
        'voter_id': str(uuid.uuid4()),
        'campaign_id': 1,
        'candidate_id': 2,
        'timestamp': str(time.time())
    }).__dict__)
