import time
from hashlib import sha256


class TransactionModel:

    def __init__(self, address_from, address_to, amount):
        self.address_from = sha256(address_from.encode()).hexdigest()
        self.address_to = sha256(address_to.encode()).hexdigest()
        self.amount = amount
        self.time = time.time()

    def json(self):
        return {'address_from': self.address_from, 'address_from': self.address_to, 'amount': self.amount, 'time': self.time}
