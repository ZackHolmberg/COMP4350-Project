"""A modul containing the transaction class for the blockchain"""
import json

class Transaction:
    """The transaction class"""
    def __init__(self, from_address, to_address, amount, timestamp, id_, signature):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = timestamp
        self.id = id_
        self.signature = signature

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
