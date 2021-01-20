from collections import deque
from helpers import hash_vote
import uuid
import time
import json
from block import Block
from helpers import GENESIS_BLOCK_VALUES
from constants import SHARD_SIZE


class Shard:
    def __init__(self, id, initial_block, is_genesis):
        self.id = id
        self.is_genesis = is_genesis

        # Initial block can be the genesis block in the case of the first shard. Otherwise, we will use the 
        # last block of the previous shard. This way we can make sure that the blockchain is continuous and
        # every block's hash depends on the previous hash and the content of the block.
        self.initial_block = initial_block
        self.shard = deque([initial_block]) if is_genesis else deque([])

    # Method used to add a new block to the shard. Takes an array of votes as input.
    def add_block(self, votes):
        # Get last block in the chain.
        prev_block = self.shard[-1] if len(
            self.shard) > 0 else self.initial_block
        # Create new block.
        new_block = Block.create(prev_block, votes)
        # Add new block to chain.
        self.shard.append(new_block)

    # Checks if voter has already voted given their voter_id and the campaign_id they voted in.
    def has_voted(self, voter_id, campaign_id):
        # Skip genesis block in the case of the first shard.
        start = 1 if self.is_genesis else 0
        for i in range(start, len(self.shard)):
            for vote in self.shard[i].votes:
                if vote['voter_id'] == voter_id and vote['campaign_id'] == campaign_id:
                    return True
        return False

    # Validates the incoming shard and replaces the current shard if valid.
    def replace_shard(self, shard):
        initial_block = shard["last_block"]
        shard = shard["data"]
        if not Shard.isShardValid(shard, initial_block, self.is_genesis):
            return None
        vote_blocks = deque()
        for block in shard:
            vote_blocks.append(Block(
                block['prev_hash'], block['timestamp'], block['votes']))
        self.shard = vote_blocks
        return self

    # Checks shard validity by comparing genesis blocks (in the case of the initial shard), and rehashing the votes to retrieve
    # validate the block hash.
    @staticmethod
    def isShardValid(shard, initial_block, is_genesis=False):
        if is_genesis:
            # Check that the genesis block matches
            original_genesis_block = Block.genesis_block().get_dict()
            incoming_genesis_block = shard[0]
            # Deep compare block values.
            for key in original_genesis_block:
                if key not in incoming_genesis_block:
                    return False

            for key in incoming_genesis_block:
                if key not in original_genesis_block:
                    return False

        # Check that the blocks are valid.
        start = 1 if is_genesis else 0
        for i in range(start, len(shard)):
            current_block = shard[i]
            prev_hash = shard[i -
                              1]['hash'] if i > 0 else initial_block['hash']
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

    # Prints block data in a nice format.
    def print(self):
        for i in range(len(self.shard)):
            print("Block #" + str(i + 1))
            print("Hash:", self.shard[i].merkle_root_hash)
            print("Previous Hash:", self.shard[i].prev_hash)
            print("Timestamp:", self.shard[i].timestamp)
            print("Votes:", json.dumps(self.shard[i].votes))
            print("------------------------------------")

    # Calculates the stats for a particular shard.
    def get_stats(self):
        stats = {}
        start = 1 if self.is_genesis else 0
        for i in range(start, len(self.shard)):
            block = self.shard[i]
            # Loop over votes inside a block.
            for vote_info in block.votes:
                campaign_id = vote_info['campaign_id']
                candidate_id = vote_info['candidate_id']
                if campaign_id not in stats:
                    stats[campaign_id] = {}
                stats[campaign_id][candidate_id] = stats[campaign_id].get(
                    candidate_id, 0) + 1
        return stats

    # Returns the shard data in json format. Used in API endpoint for displaying data on the web app.
    def get_json(self):
        result = []
        for block in self.shard:
            result.append(block.get_dict())
        return {"id": self.id, "count": len(self.shard), "last_block": self.initial_block.get_dict(), "data": result}

    # Retrieves number of blocks in the shard.
    def get_block_count(self):
        return len(self.shard)


if __name__ == '__main__':
    shard = Shard(Block.genesis_block(), True)
    voter = str(uuid.uuid4())
    shard.add_block([{
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

    shard2 = Shard(Block.genesis_block(), True)
    shard2.add_block([
        GENESIS_BLOCK_VALUES,
        {
            'voter_id': str(uuid.uuid4()),
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
    shard2.add_block([
        GENESIS_BLOCK_VALUES,
        {
            'voter_id': str(uuid.uuid4()),
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

    print(shard.replace_shard(shard2.get_json()))
    print(shard.get_block_count())
