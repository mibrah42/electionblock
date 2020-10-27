from hashlib import sha256
import json

# Constants.
STARTING_DIFFICULTY = 3

MINING_RATE = 1000

GENESIS_BLOCK_VALUES = {
    'hash': 'GENESIS_HASH',
    'prev_hash': 'GENESIS_PREV_HASH',
    'timestamp': 00000000,
    'vote_info': {},
    'difficulty': STARTING_DIFFICULTY,
    'nonce': 0
}

# Helper methods.
def hash_vote(prev_hash, current_time, vote_info, difficulty, nonce):
    vote_info_json_string = json.dumps(vote_info)
    combined_data = prev_hash + current_time + vote_info_json_string + str(difficulty) + str(nonce)
    return sha256(combined_data.encode()).hexdigest()
