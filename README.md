# CSICoin
## Introduction
A new Blockchain infrastructure capable to make transaction between two addresses.
## About the application

Our goal is to build a simple Restful Api that allows users to make transaction between addresses.

#### The structure of the **Transaction**
we'll store the transaction in a JSON format.

The transaction object fields :
1) address_from ( hashed value to simulate the user public key )
2) address_to ( hashed value to simulate the user public key )
3) amount
4) time

#### The structure of the **Block**
The Block contain those field saved in a JSON format:
1) index
2) timestamp ( Time when we generate the block)
3) transactions ( List of transaction added to the block )
4) previous_hash ( hash of the previous block in the chain)
5) hash ( hash of the block generated on the init )
6) nonce ( the proof value )

#### Chain the blocks

The blockchain is the collection of blocks,
and each block is linked to the previous block by the previous_hash field.

###### Why using the previous hash ?
To prevent the changes of the previous blocks.

- When the hacker change the previous block the hash of the block would change,
leading to a mismatch with the previous_hash field in the next block.

###### What about the first block?
The first block is called the genesis block. We add it automaticly when initializing the Block Chain of each peers.

#### Proof of Work algorithm

A Proof-of-Work algorithm is an algorithm that generates an item that is difficult to create but easy to verify.
The item is called the proof and, as it sounds, it is proof that a computer performed a certain amount of work.

So we're going to introduce a new field in our block called nonce.
A nonce is a number that we'll keep on changing until we get a value that satisfies our constraint:
- Higher than the last proof of work on the blockchain ( we start counting from the last proof value)
- A multiple of 7 and of the length of the last block json representation 

By using the proof the block cannot be changed without redoing the work, As later blocks are chained after it, the work to change the block would include redoing all the blocks after it.


#### Mining

The process of putting the unconfirmed transactions in a block and computing Proof of Work is known as the mining of blocks.
Once the nonce (proof) satisfying our constraints, we can say that a block has been mined, and the block is put into the blockchain.


After that We need to announce to the network that it has mined a block so that everyone can update their blockchain.

> And the person how mined a block will receive 1 coin, and this transaction will be added to the block.

#### Establish consensus and decentralization
Even though we're linking block with hashes, we still can't trust a single entity.
We need multiple nodes to maintain our blockchain.

There's a problem with multiple nodes, the copy of chains can be different.
In that case, we need to agree upon some version of the chain to maintain the integrity of the entire system.
We need to achieve consensus.

A simple consensus algorithm could be to agree upon the longest valid chain when the chains of different nodes diverge.

## About the Restful API
This application is accessible through a Restful API interface.

#### Initial the 10000 coins
We can initial the coins by using this route :
```
GET http://localhost:5000/initial_coin HTTP/1.1 
```
This route it can be used once , and return an error when used more : `{ "message": "can not change the number of coins" }`
 
#### Make transaction between two addresses
The new transactions are initially stored in a pool of unconfirmed transactions.
We can make transaction using this end point :
```
POST /transaction HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
    "address_to": "a",
    "address_from": "b",
    "amount": 2
}
```
#### Add new nodes
To add new node to the network (peers) , we can use this endpoint:
```
POST /add_nodes HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
 "node_url": "127.0.0.1:8000"
}
```
#### Mine

User can mine blocks on the block chain using this route:
```
GET /mine HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```
The respond will be the index of the minded block.
In case we don't have unconfirmed transactions, the response will be `{"message": "No transactions to mine"}`

###### Proof of work
In the Mining function we run the `pow algorithm` to generate the proof number saved in the nonce field of the block.
After that we add the block to the chain using add_to_block function.

the proof of work condition :
```
    difficulty = 7
    # new_nonce = counting from the last proof + 1
    def pow_definition(self, new_nonce):
        return new_nonce % BlockchainModel.difficulty == 0 and new_nonce % len(json.dumps(self.last_block.__dict__, sort_keys=True)) == 0
```
###### Broadcast the new block
We broadcast the new block to the nodes in the networks, we request a post call to the add_block endpoint of each node in the network.

we check if the new block is valid(by checking if previous_hash field is equal to the hash of the previous block and if the proof is valid )
```
POST /add_block HTTP/1.1
Host: localhost:8000
Content-Type: application/json

 {
    "hash": "5198497e3ce7d8561cd563bff0bd2baa3357b64620fbfa908fe7da9d3a8166d4",
    "index": 1,
    "nonce": 175,
    "previous_hash": "2ffa737a7553b66bc690f9489757bcac7d14a0ab1736613a487ec34b69288e16",
    "timestamp": 1531591071.5817795,
    "transactions": [
        {
            "address_from": "3e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d",
            "address_to": "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
            "amount": 2,
            "time": 1531591067.7787225
        }
    ]
 }
 ```

#### Chain
To see the blockchain we can use this endpoint :
```
GET /chain HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```

before returning the blockchain result we use the `consensus algorithm` to choose the longest valid chain( valid proof ).

response :
```
{
    "chain": [
        {
            "hash": "ceb0a98337a2b103ff9ea1357c313cd512d82ac945c5728950a5c25880cb24c5",
            "index": 0,
            "nonce": 1,
            "previous_hash": "0",
            "timestamp": 1531570803.0894673,
            "transactions": []
        },
        {
            "hash": "d05feb2df6c69ac36d5933bfa948543375c145e260b5d56e7bbaa90f85d1480b",
            "index": 1,
            "nonce": 175,
            "previous_hash": "ceb0a98337a2b103ff9ea1357c313cd512d82ac945c5728950a5c25880cb24c5",
            "timestamp": 1531570813.848194,
            "transactions": [
                {
                    "address_from": "3e23e8160039594a33894f6564e1b1348bbd7a0088d42c4acb73eeaed59c009d",
                    "address_to": "ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb",
                    "amount": 2,
                    "time": 1531570810.3708248
                },
                {
                    "address_from": "3009be769fb8f956e8413ee9f3e0836e34968bc40457d0a10c549d2edcf00cc1",
                    "address_to": "8b133a3868993176b613738816247a7f4d357cae555996519cf5b543e9b3554b",
                    "amount": 1,
                    "time": 1531570813.8481722
                }
            ]
        }
    ],
    "length": 2
}
```
## Instructions to run
#### Python Version 
In this project we are using `python 3.6`
#### Create an environment
Create a venv folder within the project folder:
```
cd coin
python3 -m venv venv
```
#### Activate the env
Before you work on your project, activate the corresponding environment:
```
. venv/bin/activate
```
#### Install Requirements
Within the activated environment, use the following command to install the list of requirements:
```
pip install -r requirements.txt
```
#### Debug Mode
Run our application:
```
export FLASK_APP=app
export FLASK_RUN_PORT=5000
flask run
```
to test the application using to node
```
export FLASK_APP=app
export FLASK_RUN_PORT=8000
flask run
```

## Examples
#### Test the Application using different node in the network
1) Run the application using the port 5000
2) Run on new terminal tab the same application using port 8000
3) We add new Node to the application (the node of the port 8000 )
4) Add transaction on the node 5000
5) Mining on the node 5000

    >>Testing the Broadcast of the block
6) We check the chain of the node 5000, we found the block is added to chain
7) We check the chain of the node 8000, we found the same block added

    >>Testing the consensus algorithm ( valid chain and longest chain)
8) we add more transaction on the node of port 5000 until the chain be longer than the one app port 8000
9) We check the chain of the node 5000, we found we have the same chain ( the consensus algo update the chain )