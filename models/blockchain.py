import time
from models.block import BlockModel


class BlockchainModel:

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        # A function to generate the first block
        genesis_block = BlockModel(0, time.time(), [], "0")
        self.chain.append(genesis_block)
