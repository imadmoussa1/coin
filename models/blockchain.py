import json
import time
import requests
from models.block import BlockModel


class BlockchainModel:
    # difficulty of our PoW algorithm
    difficulty = 7

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.genesis_block()

    # A function to generate the first block
    def genesis_block(self):
        genesis_block = BlockModel(0, 0, [], "0")
        self.chain.append(genesis_block)

    # function use to add the created transaction to unconfirmed transactions
    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    # the pow condition to generate the proof
    def pow_definition(self, new_nonce):
        return new_nonce % BlockchainModel.difficulty == 0 and new_nonce % len(json.dumps(self.last_block.__dict__, sort_keys=True)) == 0

    # function to return the last block in the chain
    @property
    def last_block(self):
        return self.chain[-1]

    # This function to add the pending transactions to the chain, and use the pow
    def mine(self, peers):
        last_block = self.last_block
        new_block = BlockModel(index=last_block.index + 1,
                               transactions=self.unconfirmed_transactions,
                               timestamp=time.time(),
                               previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        # broadcast the new block to network peers
        self.broadcast_new_block(new_block, peers)
        return new_block.index

    # proof of work function to generate the number use as proof
    def proof_of_work(self, block):
        new_nonce = self.last_block.nonce + 1
        while not self.pow_definition(new_nonce):
            new_nonce += 1
        return new_nonce

    # A function that adds the block to the chain after checking if the block is valid
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not self.pow_definition(block.nonce):
            return False
        block.nonce = proof
        self.chain.append(block)
        return True

    # use to validate the chain ( valid proof and valid hash for each block in chain)
    @staticmethod
    def check_chain_validity(chain):
        result = True
        previous_hash = "0"
        previous_block_len = 1
        for block in chain:
            o_block = BlockModel(index=block['index'], timestamp=block['timestamp'], transactions=block['transactions']
                                 , previous_hash=block['previous_hash'])
            o_block.hash = block['hash']
            o_block.nonce = block['nonce']
            block_hash = o_block.hash
            if not o_block.nonce % BlockchainModel.difficulty == 0 \
                    and o_block.nonce % previous_block_len == 0\
                    or previous_hash != o_block.previous_hash:
                result = False
                break
            o_block.hash, previous_hash, previous_block = block_hash, block_hash, o_block
            previous_block_len = len(json.dumps(previous_block.__dict__, sort_keys=True))
        return result

    @staticmethod
    def convert_chain_from_json_to_object(chain):
        new_chain = []
        for block in chain:
            o_block = BlockModel(index=block['index'], timestamp=block['timestamp'], transactions=block['transactions']
                                 , previous_hash=block['previous_hash'])
            o_block.hash = block['hash']
            o_block.nonce = block['nonce']
            new_chain.append(o_block)
        return new_chain

    # function to call the add_block endpoint of the peers node ( broadcast the new block)
    @staticmethod
    def broadcast_new_block(block, peers):
        for peer in peers:
            url = "http://{}/add_block".format(peer)
            requests.post(url, data=json.dumps(block.__dict__, sort_keys=True), headers={'Content-type': 'application/json'})
