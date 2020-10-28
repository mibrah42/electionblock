from collections import deque
from helpers import hash_vote
from VoteBlock import VoteBlock
import uuid
import time
import json

class Blockchain:
    def __init__(self):
        self.blockchain = deque([VoteBlock.genesis_block()])
    
    def add_block(self, vote_info):
        # Get last block in the chain.
        prev_block = self.blockchain[-1]
        # Mine new block.
        new_block = VoteBlock.mine(prev_block, vote_info)
        # Add new block to chain.
        self.blockchain.append(new_block)
    
    def replace_blockchain(blockchain):
        if len(blockchain) <= len(self.blockchain):
            # New blockchain has a shorter length (invalid).
            return
        if not Blockchain.isBlockchainValid(blockchain):
            return
        print("Replacing chain...")
        self.blockchain = blockchain
    
    def print(self):
        for i in range(len(self.blockchain)):
            print("Block #" + str(i + 1))
            print("Hash:", self.blockchain[i].hash)
            print("Previous Hash:", self.blockchain[i].prev_hash)
            print("Timestamp:", self.blockchain[i].timestamp)
            print("Vote Info:", json.dumps(self.blockchain[i].vote_info))
            print("Difficulty:", self.blockchain[i].difficulty)
            print("Nonce:", self.blockchain[i].nonce)
            print("------------------------------------")
    
    def getJSON(self):
        result = []
        for block in self.blockchain:
            result.append(block.__dict__)
        return result

    @staticmethod
    def isBlockchainValid(blockchain):
        # Check that the genesis block matches.
        original_genesis_block = json.dumps(VoteBlock.genesis_block())
        incoming_genesis_block = json.dumps(blockchain[0])
        if original_genesis_block != incoming_genesis_block:
            return False
        
        # Check that the rest of the blocks are valid.
        for i in range(1, len(blockchain)):
            current_block = blockchain[i]
            prev_hash = blockchain[i - 1].hash
            prev_difficulty = blockchain[i - 1].difficulty
            if abs(prev_difficulty - current_block.difficulty) > 1:
                return False    
            # Check if previous hash matches the current block's previous hash.
            if prev_hash != current_block.prev_hash:
                return False
            # Recalculate hash given block values.
            recalculated_hash = hash_vote(prev_hash, current_block.timestamp, current_block.vote_info, prev_block.difficulty, prev_block.nonce)
            # Check if recalculated hash matches the current block's hash.
            if recalculated_hash != current_block.hash:
                return False 
            return True
        
if __name__ == '__main__':
    blockchain = Blockchain()
    blockchain.add_block({
        'voter_id': str(uuid.uuid4()),
        'campaign_id': 2,
        'candidate_id': 4,
        'timestamp': str(time.time())
    })
    blockchain.add_block({
        'voter_id': str(uuid.uuid4()),
        'campaign_id': 1,
        'candidate_id': 3,
        'timestamp': str(time.time())
    })
    blockchain.print()