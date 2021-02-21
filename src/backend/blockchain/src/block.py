from hashlib import sha256
import json


class Block:
    def __init__(self, index, transaction, timestamp, prevHash):

        self.index = int(index)
        self.transaction = transaction
        self.timestamp = str(timestamp)
        self.prevHash = str(prevHash)
        self.nonce = int(0)
        self.hash = str(self.calculateHash())
        print("In constructor", type(self.transaction))

    def calculateHash(self):

        # toHash = json.dumps(self.index, self.transaction.toJSON(
        # ), self.timestamp, self.prevHash, self.nonce, self.hash)
        print("In calculateHash", type(self.transaction))
        toHash = json.dumps(self.transaction.toJSON())
        return sha256(toHash.encode()).hexdigest()
