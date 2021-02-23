from hashlib import sha256
import json


class Block:
    def __init__(self, index, transaction, timestamp, hash, prev_hash):

        self.index = int(index)
        self.transaction = transaction
        self.timestamp = str(timestamp)
        self.prev_hash = str(prev_hash)
        self.nonce = int(0)
        self.hash = str(hash)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
