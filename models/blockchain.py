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
        genesis_block = BlockModel(0, 0, [], "0")
        self.chain.append(genesis_block)

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def pow_definition(self, new_nonce):
        # the pow condition to generate the proof
        return new_nonce % BlockchainModel.difficulty == 0 and new_nonce % len(json.dumps(self.last_block.__dict__, sort_keys=True)) == 0

    @property
    def last_block(self):
        return self.chain[-1]

    def mine(self, peers):
        # This function to add the pendingtransactions to the blockchain by adding them to the block
        last_block = self.last_block

        new_block = BlockModel(index=last_block.index + 1,
                               transactions=self.unconfirmed_transactions,
                               timestamp=time.time(),
                               previous_hash=last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)

        self.unconfirmed_transactions = []
        self.announce_new_block(new_block, peers)
        return new_block.index

    def proof_of_work(self, block):
        # proof of work algo
        new_nonce = self.last_block.nonce + 1

        while not self.pow_definition(new_nonce):
            new_nonce += 1
        return new_nonce

    def add_block(self, block, proof):
        # A function that adds the block to the chain
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        block.nonce = proof
        self.chain.append(block)
        return True

    def check_chain_validity(self, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            o_block = BlockModel(index=block['index'], timestamp=block['timestamp'], transactions=block['transactions']
                                 , previous_hash=block['previous_hash'])
            o_block.hash = block['hash']
            o_block.nonce = block['nonce']
            block_hash = o_block.hash

            if not self.is_valid_proof(o_block, o_block.hash) or previous_hash != o_block.previous_hash:
                result = False
                break

            o_block.hash, previous_hash = block_hash, block_hash
        return result

    def is_valid_proof(self, block, block_hash):
        return self.pow_definition(block.nonce) and block_hash == block.generate_hash_block()

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

    def announce_new_block(self, block, peers):
        for peer in peers:
            url = "http://{}/add_block".format(peer)
            requests.post(url, data=json.dumps(block.__dict__, sort_keys=True), headers={'Content-type': 'application/json'})
