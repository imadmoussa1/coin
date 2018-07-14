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

# the address to other participating members of the network
peers = set()

# endpoint to submit a new transaction.
@app.route('/initial_coin', methods=['GET'])
def initial_coin():
    global coin_nb
    if coin_nb is None:
        coin_nb = 10000
        return json.dumps({'message': "nb of coin set : 10000"}), 200
    return jsonify({'message': "can not change the number of coins"}), 400


# endpoint to submit a new transaction.
@app.route('/transaction', methods=['POST'])
def new_transaction():
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
    # make sure we've the longest chain
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return jsonify({"length": len(chain_data), "chain": chain_data}), 200


# endpoint to request the node to mine the unconfirmed transactions.
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    if not blockchain.unconfirmed_transactions:
        return jsonify({'message': "No transactions to mine"})
    transaction = TransactionModel("network", "miner", 1)
    blockchain.add_new_transaction(transaction.json())
    result = blockchain.mine(peers)
    return jsonify({'message': "Block #{} is mined.".format(result)})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
