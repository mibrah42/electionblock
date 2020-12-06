import pickle


class BlockchainFileManager:
    def __init__(self, filename):
        self.filename = filename

    def serialize_blockchain(self, blockchain):
        with open(self.filename, 'wb') as f:
            pickle.dump(blockchain, f)

    def get_blockchain(self):
        with open(self.filename, 'rb') as f:
            blockchain = pickle.load(f)
            return blockchain


if __name__ == '__main__':
    manager = BlockchainFileManager('blockchain.db')
    manager.serialize_blockchain([{'vote': 1}, {'vote': 2}, {'vote': 3}])
    blockchain = manager.get_blockchain()
    print(blockchain)
