from hashlib import sha256
import json
import time

from flask import Flask, request


class Transaction:
    def __init__(self, toAddress, fromAddress, amount):
        self.toAddress = toAddress
        self.fromAddress = fromAddress
        self.amount = amount

    def toJSON(self):
        return json.dumps(self)


class Block:
    def __init__(self, index, transaction, timestamp, prevHash):

        self.index = index
        self.transaction = transaction
        self.timestamp = timestamp
        self.prevHash = prevHash
        self.nonce = 0
        self.hash = self.calculateHash()

    def calculateHash(self):

        toHash = json.dumps(self.__dict__, sort_keys=True)
        return sha256(toHash.encode()).hexdigest()


class Blockchain:

    wallets = {}

    def __init__(self):

        self.chain = []
        self.initializeChain()

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

        # create the genesis block
        genesisBlock = Block(0, [], time.time(), "0")

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

    # The following three methods will likely be taken out and moved to the transaction service or front end

    def proofOfWork(self, block):

        block.nonce = 0

        proof = block.calculateHash()
        while not proof.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            proof = block.calculateHash()

        return proof

    def addTransaction(self, transaction):
        self.transactionQueue.append(transaction)

    def mine(self):

        last_block = self.getLastBlock

        newBlock = Block(index=last_block.index + 1,
                         transactions=self.transactionQueue,
                         timestamp=time.time(),
                         prevHash=last_block.hash)

        proof = self.proofOfWork(newBlock)
        self.appendBlockToChain(newBlock, proof)

        return newBlock.index


blockchain = Blockchain()
