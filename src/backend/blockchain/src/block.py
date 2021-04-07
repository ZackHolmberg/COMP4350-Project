import json
from .transaction import Transaction

class Block:
    def __init__(self, index, transaction, nonce, hash, prev_hash, miner_id, reward_amount):

        self.index = int(index)
        self.transaction = transaction
        self.prev_hash = str(prev_hash)
        self.nonce = int(nonce)
        self.hash = str(hash)
        self.miner_id = str(miner_id)
        self.reward_amount = int(reward_amount)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
    
    def from_json(data):
        transaction_data = data["transaction"]
        transaction_obj = Transaction.from_json(transaction_data)
        return Block(
            data["index"],
            transaction_obj,
            data["nonce"],
            data["hash"],
            data["prev_hash"],
            data["miner_id"],
            data["reward_amount"]
        )


