import json
import requests
from flask import Flask, request, jsonify
from flask import json
from flask_restful import Resource, reqparse
from models.block import BlockModel
from models.transaction import TransactionModel
from models.blockchain import BlockchainModel

app = Flask(__name__)

# the node's copy of blockchain
blockchain = BlockchainModel()
coin_nb = None
transaction_amount = []

# the node address of the network
peers = set()


# endpoint to initial the coins.
@app.route('/initial_coin', methods=['GET'])
def initial_coin():
    global coin_nb
    if coin_nb is None:
        coin_nb = 10000
        return json.dumps({'message': "nb of coin set : 10000"}), 200
    return jsonify({'message': "can not change the number of coins"}), 400


# endpoint to create new transaction.
@app.route('/transaction', methods=['POST'])
def add_transaction():
    parser = reqparse.RequestParser()
    parser.add_argument('address_from', type=str, required=True, help="Invalid transaction, address_from is missing")
    parser.add_argument('address_to', type=str, required=True, help="Invalid transaction, address_to is missing ")
    parser.add_argument('amount', type=int, required=True, help="Invalid transaction, amount is missing")
    data = parser.parse_args()
    transaction_amount.append(data['amount'])
    transaction = TransactionModel(**data)
    blockchain.add_new_transaction(transaction.json())
    return jsonify(transaction.json()), 201


# endpoint to return the chains in the block.
@app.route('/chain', methods=['GET'])
def get_chain():
    # make sure we've the longest chain when we have nodes
    consensus()
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return jsonify({"length": len(chain_data), "chain": chain_data}), 200


# endpoint to mine the unconfirmed transactions.
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    if not blockchain.unconfirmed_transactions:
        return jsonify({'message': "No transactions to mine"})
    transaction = TransactionModel("network", "miner", 1)
    blockchain.add_new_transaction(transaction.json())
    result = blockchain.mine(peers)
    return jsonify({'message': "Block #{} is mined.".format(result)})


# endpoint to add new peers to the network.
@app.route('/add_nodes', methods=['POST'])
def add_nodes():
    parser = reqparse.RequestParser()
    parser.add_argument('node_url', type=str, required=True, help="Invalid transaction, node_url is missing")
    data = parser.parse_args()
    nodes = data['node_url']
    if not nodes:
        return jsonify({'message': "Invalid data"}), 400

    peers.add(nodes)
    return jsonify({'message': "Success"}), 201


# end point to create new block used when the peers broadcast the mined block
@app.route('/add_block', methods=['POST'])
def validate_and_add_block():
    block_data = request.get_json()
    block = BlockModel(index=block_data["index"], transactions=block_data["transactions"],
                       timestamp=block_data["timestamp"],
                       previous_hash=block_data["previous_hash"])
    block.hash = block_data['hash']
    proof = block_data['nonce']
    added = blockchain.add_block(block, proof)

    if not added:
        return jsonify({'message': "The block was discarded by the node"}), 400

    return jsonify({'message': "Block added to the chain"}), 201


# consnsus algorithm. to check the longer valid chain, and replace the old chain with it.
def consensus():
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)
    for node in peers:
        response = requests.get('http://{}/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain
    if longest_chain:
        blockchain.chain = BlockchainModel.convert_chain_from_json_to_object(chain)
        return True
    return False


if __name__ == '__main__':
    app.run(port=5000, debug=True)
