from flask import Flask, request
from models.blockchain import BlockchainModel

app = Flask(__name__)

# the node's copy of blockchain
blockchain = BlockchainModel()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
