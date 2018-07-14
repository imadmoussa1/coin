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
The first block is called the genesis block. We add it automaticly when initializing the Block Chain.

#### Proof of Work algorithm

A Proof-of-Work algorithm is an algorithm that generates an item that is difficult to create but easy to verify.
The item is called the proof and, as it sounds, it is proof that a computer performed a certain amount of work.

So we're going to introduce a new field in our block called nonce.
A nonce is a number that we'll keep on changing until we get a value that satisfies our constraint:
- Higher than the last proof of work on the blockchain
- A multiple of 7 and of the length of the last block json representation 

By using the proof the block cannot be changed without redoing the work, As later blocks are chained after it, the work to change the block would include redoing all the blocks after it.


#### Mining

The process of putting the unconfirmed transactions in a block and computing Proof of Work is known as the mining of blocks.
Once the nonce (proof) satisfying our constraints is figured out, we can say that a block has been mined, and the block is put into the blockchain.

> And the person how mined a block will receive 1 coin, and this transaction will be added to the block.
## About the Restful API
This application is accessible through a Restful API interface , using Postman .

#### Initial the 10000 coins
We can initial the coins by using this route :
```
GET http://localhost:5000/initial_coin HTTP/1.1 
```
This route it can be used once , and return an error when used more : `{ "message": "can not change the number of coins" }`
 
#### Make transaction between two addresses
The new transactions are initially stored in a pool of unconfirmed transactions.
To make transaction we should use this route :
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

#### Mine

User can mine blocks on the block chain using this route:
```
GET /mine HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```
The respond will be the index of the minded block.
In case we don't have unconfirmed transactions, the response will be `{"message": "No transactions to mine"}`

#### Chain 

To see the blockchain mined till now we can use this route :
```
GET /chain HTTP/1.1
Host: localhost:5000
Content-Type: application/json
```
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
python app.py
```