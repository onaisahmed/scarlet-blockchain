import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.createBlock(proof=1, previousHash='0')  # Creating a Genesis block
        self.nodes = set()
        
    def createBlock(self, proof, previousHash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previousHash': previousHash,
            'transactions': self.transactions
        }
        self.transactions = []
        self.chain.append(block)
        return block
    
    def getPreviousBlock(self):
        return self.chain[-1]
    
    def proofOfWork(self, previousProof):
        newProof = 1
        checkProof = False
        while not checkProof:
            hashOperation = hashlib.sha256(str(newProof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] == '0000':
                checkProof = True
            else:
                newProof += 1   
        return newProof 
    
    def hash(self, block):
        encodedBlock = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            currBlock = chain[blockIndex]
            if currBlock['previousHash'] != self.hash(previousBlock):
                return False
            previousProof = previousBlock['proof']
            currProof = currBlock['proof']
            hashOperation = hashlib.sha256(str(currProof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] != '0000':
                return False
            previousBlock = currBlock
            blockIndex += 1
        return True
    
    def addTransaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        
        previousBlock = self.getPreviousBlock()
        return previousBlock['index'] + 1
    
    def addNode(self, address):
        parsedUrl = urlparse(address)
        self.nodes.add(parsedUrl.netloc)
        return parsedUrl.netloc
    
    def replaceChain(self):
        network = self.nodes
        longestChain = None
        highestChainLength = len(self.chain)
        for node in network:
            response = requests.get(f'{node}/get-chain')
            if response.status_code == 200:
                currentChain = response.json()['chain']
                currentChainLength = response.json()['length']
                if currentChainLength > highestChainLength and self.isChainValid(currentChain):
                    longestChain = currentChain
                    highestChainLength = currentChainLength
        if longestChain:
            self.chain = longestChain
            return True
        return False
