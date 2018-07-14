import json
import time
from models.block import BlockModel


class BlockchainModel:
    # difficulty of our PoW algorithm
    difficulty = 7

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # A function to generate the first block
        genesis_block = BlockModel(0, time.time(), [], "0")
        self.chain.append(genesis_block)

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)
