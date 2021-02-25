import json


class Transaction:

    def __init__(self,_id, from_address, to_address, amount, signature):
        self.to_address = to_address
        self.from_address = from_address
        self.amount = amount

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)
