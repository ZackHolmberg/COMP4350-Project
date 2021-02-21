import json


class Transaction:

    def __init__(self, toAddress, fromAddress, amount):
        self.toAddress = toAddress
        self.fromAddress = fromAddress
        self.amount = amount

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
