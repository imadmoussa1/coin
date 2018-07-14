from hashlib import sha256
import json


class BlockModel:
    def __init__(self, index, timestamp, transactions,  previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.generate_hash_block()
        self.nonce = 0

    # generate the hash of the block contents.
    def generate_hash_block(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256((str(self.index) +
                      str(self.timestamp) +
                      self.previous_hash +
                      str(block_string)).encode()).hexdigest()
