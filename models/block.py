from hashlib import sha256
import json


class BlockModel:
    def __init__(self, index, timestamp, transactions,  previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.generate_hash_block()

    def generate_hash_block(self):
        # generate the hash of the block contents.

        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
