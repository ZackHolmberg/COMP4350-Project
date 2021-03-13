import json

class Block:
    def __init__(self, index, transaction, timestamp, nonce, hash, prev_hash, miner_id, rewardAmount):

        self.index = int(index)
        self.transaction = transaction
        self.timestamp = str(timestamp)
        self.prev_hash = str(prev_hash)
        self.nonce = int(nonce)
        self.hash = str(hash)
        self.miner_id = str(miner_id)
        self.rewardAmount = int(rewardAmount)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
