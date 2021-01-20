from collections import OrderedDict
from hashlib import sha256
import json

# Initial block values.
GENESIS_BLOCK_VALUES = {
    'hash': 'GENESIS_HASH',
    'prev_hash': 'GENESIS_PREV_HASH',
    'timestamp': 00000000,
    'votes': []
}

# Returns a sha256 hash of a vote's data including the current_time, vote_info, and the prev_hash.
def hash_vote(prev_hash, current_time, vote_info):
    # We need to sort the keys and store them in an OrderedDict to guarantee that
    # every identical input will result in an identical hash.
    sorted_keys = sorted(list(vote_info.keys()))
    sorted_tuples = [(key, vote_info[key]) for key in sorted_keys]
    ordered_dict = OrderedDict(sorted_tuples)
    vote_info_json_string = json.dumps(ordered_dict)
    combined_data = prev_hash + current_time + vote_info_json_string
    return sha256(combined_data.encode()).hexdigest()
