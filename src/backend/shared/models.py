import json


class Transaction:
    def __init__(self, to, from, amount):
        self.toAddress = to
        self.fromAddress = from
        self.amount = amount

    def toJSON(self):
        return json.dumps(self)
