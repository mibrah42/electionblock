import time
import uuid
import math
import binascii
from helpers import GENESIS_BLOCK_VALUES, MINING_RATE, hash_vote

class VoteBlock:
    def __init__(self, prev_hash, hash, timestamp, vote_info, difficulty, nonce):
        self.prev_hash = prev_hash
        self.hash = hash
        self.timestamp = timestamp
        self.vote_info = vote_info
        self.difficulty = difficulty
        self.nonce = nonce
    
    @staticmethod
    def genesis_block():
        # Initialize genesis block with dummy values.
        return VoteBlock(GENESIS_BLOCK_VALUES['prev_hash'], GENESIS_BLOCK_VALUES['hash'], GENESIS_BLOCK_VALUES['timestamp'], GENESIS_BLOCK_VALUES['vote_info'], GENESIS_BLOCK_VALUES['difficulty'], GENESIS_BLOCK_VALUES['nonce'])

    @staticmethod
    def mine(prev_block, vote_info):
        nonce = 0
        new_hash = None
        current_time = None
        difficulty = prev_block.difficulty
        
        while new_hash is None or str(bin(int(new_hash, 16)).zfill(16))[3:difficulty + 3] != ('0' * difficulty):
            nonce += 1
            current_time = str(time.time())
            difficulty = VoteBlock.modify_difficulty(prev_block, current_time)
            new_hash = hash_vote(prev_block.hash, current_time, vote_info, difficulty, nonce)

        return VoteBlock(prev_block.hash, new_hash, current_time, vote_info, difficulty, nonce)

    @staticmethod
    def modify_difficulty(vote_block, timestamp):
        # We can't have negative values for difficulty. 
        if vote_block.difficulty < 1:
            return 1
        time_difference = float(timestamp) - float(vote_block.timestamp)
        if time_difference > MINING_RATE:
            # The last block was mined too slowly, we need to lower the difficulty. 
            return vote_block.difficulty - 1
        return vote_block.difficulty + 1


if __name__ == "__main__":
    block = VoteBlock('prev_hash', 'hash', str(time.time()), {
        'voter_id': str(uuid.uuid4()),
        'campaign_id': 1,
        'candidate_id': 2,
        'timestamp': str(time.time())
    })

    print(block.__dict__)

    print(VoteBlock.mine(block, {
        'voter_id': str(uuid.uuid4()),
        'campaign_id': 1,
        'candidate_id': 2,
        'timestamp': str(time.time())
    }).__dict__)
