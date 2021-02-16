from hashlib import sha256
import json
import time

from flask import Flask, request


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
    # difficulty of our PoW algorithm
    difficulty = 4

    def __init__(self):

        self.transactionQueue = []
        self.chain = []
        self.createGenesisBlock()

    def createGenesisBlock(self):

        genesisBlock = Block(0, [], time.time(), "0")
        self.chain.append(genesisBlock)

    @property
    def getLastBlock(self):
        return self.chain[-1]

    def addBlock(self, block, proof):

        prevHash = self.getLastBlock.hash

        if prevHash != block.prevHash:
            return False

        if not self.validProof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def validProof(self, block, hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (hash.startswith('0' * Blockchain.difficulty) and
                hash == block.calculateHash())

    def proofOfWork(self, block):

        block.nonce = 0

        computed_hash = block.calculateHash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.calculateHash()

        return computed_hash

    def addTransaction(self, transaction):
        self.transactionQueue.append(transaction)

    # This will likely be brought out and put into the miner component of the web app
    def mine(self):

        if len(self.transactionQueue):
            return False

        last_block = self.getLastBlock

        newBlock = Block(index=last_block.index + 1,
                         transactions=self.transactionQueue,
                         timestamp=time.time(),
                         prevHash=last_block.hash)

        proof = self.proofOfWork(newBlock)
        self.addBlock(newBlock, proof)

        self.transactionQueue = []
        return newBlock.index


app = Flask(__name__)
blockchain = Blockchain()


@app.route('/chain', methods=['GET'])
def get_chain():
    chain = []
    for block in blockchain.chain:
        chain.append(block.__dict__)
    return json.dumps({"length": len(chain),
                       "chain": chain})


app.run(debug=True, port=5000)
