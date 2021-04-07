"""module containing the block class for the blockchain"""
import json

class Block:
    """class for the block object"""
    def __init__(self, index, transaction, nonce, hash, prev_hash, miner_id, reward_amount):

        self.index = int(index)
        self.transaction = transaction
        self.prev_hash = str(prev_hash)
        self.nonce = int(nonce)
        self.hash = str(hash)
        self.miner_id = str(miner_id)
        self.reward_amount = int(reward_amount)

    def toJSON(self):
        """
        creates a json string of the class

        params:
            N/A

        returns:
            A json string of class attributes
        """
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
