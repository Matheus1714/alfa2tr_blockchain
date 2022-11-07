from flask import jsonify, request
from src.models.Blockchain import Blockchain
import requests
from uuid import uuid4
from urllib.parse import urlparse

def routes(app, blockchain:Blockchain):
    
    @app.route('/mine_block', methods = ['GET'])
    def mine_block():
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        block, id = blockchain.create_block(proof, previous_hash)
        response = {
            'msg':'mine block',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }
        return jsonify(response), 200

    @app.route('/get_chain', methods = ['GET'])
    def get_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
        return jsonify(response), 200

