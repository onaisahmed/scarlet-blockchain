from flask import  jsonify, request
from app.blockchain import Blockchain
from uuid import uuid4

def create_routes(app):
    nodeAddress = str(uuid4()).replace('-', '')
    blockchain = Blockchain()

    @app.route('/mine-block', methods=['GET'])
    def mineBlock():
        previousBlock = blockchain.getPreviousBlock()
        previousProof = previousBlock['proof']
        proof = blockchain.proofOfWork(previousProof)
        previousHash = blockchain.hash(previousBlock)
        blockchain.addTransaction(sender=nodeAddress, receiver='Onais', amount=100)
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

    @app.route('/is-valid', methods=['GET'])
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

    @app.route('/add-transaction', methods=['POST'])
    def addTransaction():
        json = request.get_json()
        transactionKeys = ['sender', 'receiver', 'amount']
        if not all(key in json for key in transactionKeys):
            return 'Cannot perform transaction! Some elements are missing', 400
        blockIndex = blockchain.addTransaction(json['sender'], json['receiver'], json['amount'])
        response = {'message': f'This transaction will be added to block {blockIndex}'}
        return jsonify(response), 201

    @app.route('/connect-nodes', methods=['POST'])
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

    @app.route('/replace-chain', methods=['GET'])
    def replaceChain():
        isChainReplaced = blockchain.replaceChain()
        if isChainReplaced:
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
