from collections import deque
from helpers import hash_vote
import uuid
import time
import json
from block import Block


class Blockchain:
    def __init__(self):
        self.blockchain = deque([Block.genesis_block()])

    def add_block(self, votes):
        # Get last block in the chain.
        prev_block = self.blockchain[-1]
        # Create new block.
        new_block = Block.create(prev_block, votes)
        # Add new block to chain.
        self.blockchain.append(new_block)

    # DONE: Modify to check array of votes
    def has_voted(self, voter_id, campaign_id):
        for i in range(1, len(self.blockchain)):
            for vote in self.blockchain[i].votes:
                print("vote", vote)
                print("INFO", vote['voter_id'], voter_id,
                      vote['campaign_id'], campaign_id)
                print("INFO", type(vote['voter_id']), type(voter_id),
                      type(vote['campaign_id']), type(campaign_id))
                if vote['voter_id'] == voter_id and vote['campaign_id'] == campaign_id:
                    return True
        return False

    def replace_blockchain(self, blockchain):
        if len(blockchain) <= len(self.blockchain):
            # New blockchain has a shorter length (invalid).
            return None
        if not Blockchain.isBlockchainValid(blockchain):
            return None
        vote_blocks = deque()
        for block in blockchain:
            vote_blocks.append(Block(
                block['prev_hash'], block['timestamp'], block['votes']))
        self.blockchain = vote_blocks
        return self

    def print(self):
        for i in range(len(self.blockchain)):
            print("Block #" + str(i + 1))
            print("Hash:", self.blockchain[i].merkle_root_hash)
            print("Previous Hash:", self.blockchain[i].prev_hash)
            print("Timestamp:", self.blockchain[i].timestamp)
            print("Votes:", json.dumps(self.blockchain[i].votes))
            print("------------------------------------")

    def get_stats(self):
        stats = {}
        for i in range(1, len(self.blockchain)):
            block = self.blockchain[i]
            # Loop over votes inside a block.
            print(block.get_dict())
            for vote_info in block.votes:
                campaign_id = vote_info['campaign_id']
                candidate_id = vote_info['candidate_id']
                if campaign_id not in stats:
                    stats[campaign_id] = {}
                stats[campaign_id][candidate_id] = stats[campaign_id].get(
                    candidate_id, 0) + 1
        return stats

    def get_json(self):
        result = []
        for block in self.blockchain:
            result.append(block.get_dict())
        return result

    @staticmethod
    def isBlockchainValid(blockchain):
        # Check that the genesis block matches.
        original_genesis_block = Block.genesis_block().get_dict()
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
            recalculated_hash = Block.get_root_hash(
                current_block['votes'], prev_hash, current_block['timestamp'])
            # Check if recalculated hash matches the current block's hash.
            if recalculated_hash != current_block['hash']:
                return False
            return True


if __name__ == '__main__':
    blockchain = Blockchain()
    voter = str(uuid.uuid4())
    blockchain.add_block([{
        'voter_id': voter,
        'campaign_id': 2,
        'candidate_id': 4,
        'timestamp': str(time.time())
    },
        {
        'voter_id': str(uuid.uuid4()),
        'campaign_id': 2,
        'candidate_id': 4,
        'timestamp': str(time.time())
    },
        {
        'voter_id': str(uuid.uuid4()),
        'campaign_id': 1,
        'candidate_id': 1,
        'timestamp': str(time.time())
    }])
    blockchain.add_block([{
        'voter_id': str(uuid.uuid4()),
        'campaign_id': 1,
        'candidate_id': 3,
        'timestamp': str(time.time())
    }])
