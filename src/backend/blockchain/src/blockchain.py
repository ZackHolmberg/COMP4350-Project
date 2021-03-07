import time
from .block import Block
from .transaction import Transaction
from .exceptions import WalletException

class Blockchain:

    difficulty = 4

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
            self.wallets[id] = 10
            return True

    def add_to_wallet(self, id, amount):
        self.check_id_present(id)
        self.wallets[id] += amount
        return self.wallets[id]

    def subtract_from_wallet(self, id, amount):
        self.check_id_present(id)
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
        empty_transaction = Transaction( "", "", 0)

        # create the genesis block
        genesis_block = Block(0, empty_transaction,
                              time.time(), "0"*self.difficulty, "0")

        # append it to the chain
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def append_block_to_chain(self, block, proof):

        prev_hash = self.get_last_block().hash

        if prev_hash != block.prev_hash:
            return False

        if not self.valid_proof(proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def valid_proof(self, hash):
        return (hash.startswith('0' * self.difficulty))


blockchain = Blockchain()
