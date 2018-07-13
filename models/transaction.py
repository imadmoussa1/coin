import time


class TransactionModel:

    def __init__(self, user_from, user_to, amount):
        self.user_from = user_from
        self.user_to = user_to
        self.amount = amount
        self.time = time.time()

    def json(self):
        return {'user_from': self.user_from, 'user_to': self.user_to, 'amount': self.amount, 'time': self.time}
