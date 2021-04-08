from .block import Block
from .transaction import Transaction
from .exceptions import WalletException
import json

class Blockchain:

    difficulty = 4
    COINBASE_AMOUNT = 10
    SEED_AMOUNT = 10

    def __init__(self):
        self.chain = []
        self.initialize_chain()
        self.wallets = {}

    def check_id_present(self, id):
        if id not in self.wallets:
            raise WalletException("no corresponding wallet for id")

    def add_wallet(self, id):
        if id in self.wallets:
            raise WalletException("wallet ID already exists")
        else:
            self.wallets[id] = self.SEED_AMOUNT
            return True

    def add_to_wallet(self, id, amount):
        self.check_id_present(id)
        if amount < 0:
            raise WalletException("Cannot add a negative amount")
        self.wallets[id] += amount
        return self.wallets[id]

    def subtract_from_wallet(self, id, amount):
        self.check_id_present(id)
        if amount < 0:
            raise WalletException("Cannot subtract a negative amount")
        self.wallets[id] -= amount
        return self.wallets[id]

    def get_wallet_amount(self, id):
        self.check_id_present(id)
        return self.wallets[id]

    def verify_wallet_amount(self, id, amount):
        self.check_id_present(id)
        if self.wallets[id] < amount:
            return False
        else:
            return True

    def initialize_chain(self):

        # create empty transaction
        empty_transaction = Transaction("", "", 0, 0, "", "")

        # create the genesis block
        genesis_block = Block(0, empty_transaction, 0,
                              "0"*self.difficulty, "0", "miner_id", 0)

        # append it to the chain
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def build_chain_from_peer_response(self, data):
        new_chain = []
        chain = data["chain"]
        for block in chain:
            block = json.loads(block)
            new_chain.append(Block.from_json(block))
        
        if new_chain:
            self.chain = new_chain
        
    def build_wallets_from_peer_response(self, data):
        wallets = data["wallets"]
        new_wallets = {}
        for wallet in wallets:
            wallet = json.loads(wallet)
            new_wallets[wallet["umnetId"]] = wallet["amount"]
        
        if new_wallets:
            self.wallets = new_wallets

blockchain = Blockchain()
