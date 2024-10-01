# Module 2 - Create a cryptocurrency

import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.createBlock(proof = 1, previousHash = '0') # Creating a Genesis block
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
        while checkProof is False:
            hashOperation = hashlib.sha256(str(newProof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] == '0000':
                checkProof = True
            else:
                newProof +=1   
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
    
    def addTransacction(self, sender, reciever, amount):
        self.transactions.append({
            'sender': sender,
            'reciever': reciever,
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
    
app = Flask(__name__)

nodeAddress = str(uuid4()).replace('-', '') 

blockchain = Blockchain()

@app.route('/mine-block', methods=['GET'])
def mineBlock():
    previousBlock = blockchain.getPreviousBlock()
    previousProof = previousBlock['proof']
    proof = blockchain.proofOfWork(previousProof)
    previousHash = blockchain.hash(previousBlock)
    blockchain.addTransacction(sender = nodeAddress, reciever = 'Onais', amount = 100)
    block = blockchain.createBlock(proof, previousHash)
    
    response = {
            'message': 'Congratulations, you mined a block!',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previousHash': block['previousHash'],
            'transactions': block['transactions']
        }
    return jsonify(response), 200

@app.route('/get-chain', methods=['GET'])
def getChain():
    response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
    return jsonify(response), 200

@app.route('/is-valid',  methods=['GET'])
def isValid():
    valid = blockchain.isChainValid(blockchain.chain)
    if valid:
        response = {
                'message': 'All good! The blockchain is valid!'
            }
    else:
        response = {
                'message': 'Not good! The blockchain is not valid!'
            }
    return jsonify(response), 200
        

@app.route('/add-transaction',  methods=['POST'])
def addTransaction():
    json = request.get_json()
    transactionKeys = ['sender', 'reciever', 'amount']
    if not all (key in json for key in transactionKeys):
        return 'Cannot perform transaction! Some elements are missing', 400
    blockIndex = blockchain.addTransacction(json['sender'], json['reciever'], json['amount'])
    response = {'message': f'This transaction will be added to block {blockIndex}'}
    return jsonify(response), 201

@app.route('/connect-nodes',  methods=['POST'])
def connectNodes():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No nodes found', 400
    for node in nodes:
        blockchain.addNode(node)
    response = {
        'message': 'All the nodes are now connected. The Scarlet Blockchain now contains the nodes: ',
        'totalNodes': list(blockchain.nodes)
    }
    return jsonify(response), 201

@app.route('/replace-chain',  methods=['GET'])
def replaceChain():
    isChainReplace = blockchain.replaceChain()
    if isChainReplace:
        response = {
                'message': 'The nodes had different chains so the chain was replaced by the longer one!',
                'newChain': blockchain.chain
            }
    else:
        response = {
                'message': 'All good. The current chain is the largest one.',
                'actualChain': blockchain.chain
            }
    return jsonify(response), 200


app.run(host = '0.0.0.0', port = 5000)