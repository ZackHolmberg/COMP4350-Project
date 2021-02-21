import time
from .block import Block
from .transaction import Transaction


class Blockchain:

    def __init__(self):

        self.chain = []
        self.initializeChain()
        self.wallets = {}

    def addWallet(self, id):
        if id in self.wallets:
            return False
        else:
            self.wallets[id] = 0
            return True

    def addToWallet(self, id, amount):
        if id not in self.wallets:
            return -1
        else:
            self.wallets[id] += amount
            return self.wallets[id]

    def subtractFromWallet(self, id, amount):
        if id not in self.wallets:
            return -1
        if self.wallets[id] < amount:
            return -2
        else:
            self.wallets[id] -= amount
            return self.wallets[id]

    def getWalletAmount(self, id):
        if id not in self.wallets:
            return -1
        else:
            return self.wallets[id]

    # difficulty of our proof of work algorithm
    difficulty = 4

    def initializeChain(self):

        # create empty transaction
        emptyTransaction = Transaction("", "", 0)

        # create the genesis block
        genesisBlock = Block(0, emptyTransaction, time.time(), "0")

        # append it to the chain
        self.chain.append(genesisBlock)

    def getLastBlock(self):
        return self.chain[-1]

    def appendBlockToChain(self, block, proof):

        prevHash = self.getLastBlock.hash

        if prevHash != block.prevHash:
            return False

        if not self.validProof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def validProof(self, block, hash):
        return (hash.startswith('0' * Blockchain.difficulty) and
                hash == block.calculateHash())


blockchain = Blockchain()
