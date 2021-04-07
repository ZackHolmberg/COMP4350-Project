"""module containing the blockchain class and it's documents"""
from .block import Block
from .transaction import Transaction
from .exceptions import WalletException


class Blockchain:
    """The class for the blockchain object"""
    difficulty = 4
    COINBASE_AMOUNT = 10

    def __init__(self):
        self.chain = []
        self.initialize_chain()
        self.wallets = {}

    def check_id_present(self, id):
        """
        Checks to see if a wallet corresponding to the supplied id exists

        params:
            id (string): The id of the wallet

        returns:
            N/A (raises exception to be handled later)
        """
        if id not in self.wallets:
            raise WalletException("no corresponding wallet for id")

    def add_wallet(self, id):
        """
        Creates a wallet with the supplied id if it doesn't exist already.

        params:
            id (string): The id of the wallet

        returns:
            True on sucess else raises an error
        """

        if id in self.wallets:
            raise WalletException("wallet ID already exists")
    
        self.wallets[id] = 10
        return True

    def add_to_wallet(self, id, amount):
        """
        Adds an amount to the wallet corresponding to the supplied id

        params:
            id (string): The id of the wallet
            amount (float): The amount to be added

        returns:
            the string id of the affected wallet
        """

        self.check_id_present(id)
        self.wallets[id] += amount
        return self.wallets[id]

    def subtract_from_wallet(self, id, amount):
        """
        subtracts an amount from the wallet corresponding to the supplied id

        params:
            id (string): The id of the wallet
            amount (float): The amount to be subtracted

        returns:
            the string id of the affected wallet
        """
        self.check_id_present(id)
        self.wallets[id] -= amount
        return self.wallets[id]

    def get_wallet_amount(self, id):
        """
        returns the amount present in the wallet corresponding to the supplied id
        raises an error if the wallet doesn't exist

        params:
            id (string): The id of the wallet

        returns:
            The amount present in the wallet as a float
        """
        self.check_id_present(id)
        return self.wallets[id]

    def verify_wallet_amount(self, id, amount):
        """
        verifies if the wallet has enough bisoncoin present in it

        params:
            id (string): The id of the wallet
            amount (float): The amount to be verified

        returns:
            True if the wallet amount is more than the supplied a=amount else falses
        """
        self.check_id_present(id)
        if self.wallets[id] < amount:
            return False

        return True

    def initialize_chain(self):
        """
        Initializes the blockchain with a genesis block

        params:
            N/A

        returns:
            N/A
        """

        # create empty transaction
        empty_transaction = Transaction("", "", 0, 0, "", "")

        # create the genesis block
        genesis_block = Block(0, empty_transaction, 0,
                              "0"*self.difficulty, "0", "miner_id", 0)

        # append it to the chain
        self.chain.append(genesis_block)

    def get_last_block(self):
        """
        Fetches the last block added to the blockchain

        params:
            N/A

        returns:
            the last block objet in the blockchain
        """
        return self.chain[-1]


blockchain = Blockchain()
