import json


class BlockchainTransaction:

    def __init__(self, from_address, to_address, amount):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)

class ClientTransaction:

    def __init__(self, id, from_address, to_address, amount, signature):
        self.id = id
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.signature = signature

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
