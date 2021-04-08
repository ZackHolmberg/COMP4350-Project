import json


class Transaction:
    def __init__(self, from_address, to_address, amount, timestamp, id_, signature):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = timestamp
        self.id = id_
        self.signature = signature

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    def from_json(data):
        return Transaction(
            data["from_address"],
            data["to_address"],
            data["amount"],
            data["timestamp"],
            data["id"],
            data["signature"],
        )
