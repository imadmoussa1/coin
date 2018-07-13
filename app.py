import json
import time

from models.block import BlockModel
from resources.transaction import Transaction
from flask import Flask, request
import requests
from flask import json
from flask_restful import Resource, reqparse
from models.transaction import TransactionModel
from models.blockchain import BlockchainModel
app = Flask(__name__)

# the node's copy of blockchain
blockchain = BlockchainModel()

# endpoint to submit a new transaction.
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    parser = reqparse.RequestParser()
    parser.add_argument('user_from', type=str, required=True, help="Invalid transaction, user_from is missing")
    parser.add_argument('user_to', type=str, required=True, help="Invalid transaction, user_to is missing ")
    parser.add_argument('amount', type=int, required=True, help="Invalid transaction, amount is missing")
    data = parser.parse_args()

    transaction = TransactionModel(**data)
    blockchain.add_new_transaction(transaction.json())
    return json.dumps(transaction.json()), 201


if __name__ == '__main__':
    app.run(port=5000, debug=True)
