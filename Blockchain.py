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
        # Create new block.
        new_block = VoteBlock.create(prev_block, vote_info)
        # Add new block to chain.
        self.blockchain.append(new_block)

    def has_voted(self, voter_id, campaign_id):
        for i in range(1, len(self.blockchain)):
            block = self.blockchain[i]
            if block.vote_info['voter_id'] == voter_id and block.vote_info['campaign_id'] == campaign_id:
                return True
        return False

    def replace_blockchain(self, blockchain):
        print("replacing...", blockchain, flush=True)
        if len(blockchain) <= len(self.blockchain):
            # New blockchain has a shorter length (invalid).
            return None
        if not Blockchain.isBlockchainValid(blockchain):
            print("Blockchain not valid")
            return None
        print("Replacing chain...")
        vote_blocks = deque()
        for block in blockchain:
            vote_blocks.append(VoteBlock(
                block['prev_hash'], block['hash'], block['timestamp'], block['vote_info']))
        self.blockchain = vote_blocks
        return self.blockchain

    def print(self):
        for i in range(len(self.blockchain)):
            print("Block #" + str(i + 1))
            print("Hash:", self.blockchain[i].hash)
            print("Previous Hash:", self.blockchain[i].prev_hash)
            print("Timestamp:", self.blockchain[i].timestamp)
            print("Vote Info:", json.dumps(self.blockchain[i].vote_info))
            print("------------------------------------")

    def get_stats(self):
        stats = {}
        for i in range(1, len(self.blockchain)):
            block = self.blockchain[i]
            campaign_id = block.vote_info['campaign_id']
            candidate_id = block.vote_info['candidate_id']
            if campaign_id not in stats:
                stats[campaign_id] = {}
            stats[campaign_id][candidate_id] = stats[campaign_id].get(
                candidate_id, 0) + 1
        return stats

    def get_json(self):
        result = []
        for block in self.blockchain:
            result.append(block.__dict__)
        return result

    @staticmethod
    def isBlockchainValid(blockchain):
        # Check that the genesis block matches.
        original_genesis_block = VoteBlock.genesis_block().__dict__
        incoming_genesis_block = blockchain[0]

        # Deep compare block values.
        for key in original_genesis_block:
            if key not in incoming_genesis_block:
                return False

        for key in incoming_genesis_block:
            if key not in original_genesis_block:
                return False

        # Check that the rest of the blocks are valid.
        for i in range(1, len(blockchain)):
            current_block = blockchain[i]
            prev_hash = blockchain[i - 1]['hash']
            # Check if previous hash matches the current block's previous hash.
            if prev_hash != current_block['prev_hash']:
                return False
            # Recalculate hash given block values.
            recalculated_hash = hash_vote(
                prev_hash, current_block['timestamp'], current_block['vote_info'])
            # Check if recalculated hash matches the current block's hash.
            if recalculated_hash != current_block['hash']:
                print("hashes don't match", recalculated_hash,
                      current_block['hash'])
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
