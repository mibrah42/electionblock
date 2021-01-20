import pickle
import os
from os import listdir

# Used for loading and serializing shards.
class FileManager:
    def __init__(self, port):
        self.port = port
        self.folderpath = f"NODE_{port}"

    # Takes in a shard object and serializes it into a file with the shard id.
    def serialize_shard(self, shard, number):
        path = f"{self.folderpath}/shard_{number}.db"
        if not os.path.exists(self.folderpath):
            # Create folder directory if it doesn't exist.
            os.makedirs(self.folderpath)
        with open(path, 'wb') as f:
            pickle.dump(shard, f)

    # Loads shard object from file into memory given the shard id.
    def get_shard(self, number):
        path = f"{self.folderpath}/shard_{number}.db"
        if os.path.exists(path):
            with open(path, 'rb') as f:
                shard = pickle.load(f)
                return shard
        return None

    # Returns the number of shards in the file system and defaults to 0 if the folder doesn't exist.
    def get_shard_count(self):
        if os.path.exists(self.folderpath):
            return len(listdir(self.folderpath))
        else:
            return 0


if __name__ == '__main__':
    manager = FileManager(5000)
    manager.serialize_shard([{'vote': 1}, {'vote': 2}, {'vote': 3}], 0)
    shard = manager.get_shard(0)
    print(manager.get_shard_count())
