import json


class Transaction:

    def __init__(self, from_address, to_address, amount, mining):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.mining_data = mining
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
