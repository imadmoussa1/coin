class BlockModel:
    def __init__(self, index, timestamp, transactions,  previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.generate_hash_block()
