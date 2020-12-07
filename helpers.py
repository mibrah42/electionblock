from collections import OrderedDict
from hashlib import sha256
import json

GENESIS_BLOCK_VALUES = {
    'hash': 'GENESIS_HASH',
    'prev_hash': 'GENESIS_PREV_HASH',
    'timestamp': 00000000,
    'votes': []
}

# Helper methods.


def hash_vote(prev_hash, current_time, vote_info):
    sorted_keys = sorted(list(vote_info.keys()))
    sorted_tuples = [(key, vote_info[key]) for key in sorted_keys]
    ordered_dict = OrderedDict(sorted_tuples)
    vote_info_json_string = json.dumps(ordered_dict)
    combined_data = prev_hash + current_time + vote_info_json_string
    return sha256(combined_data.encode()).hexdigest()
