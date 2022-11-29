from datetime import datetime
import json

from src.utils.CryptoUtils import CryptoUtils
from src.db.Firestore import Firestore
from urllib.parse import urlparse
import requests

class Blockchain:

    crypto = CryptoUtils()
    db = Firestore()

    def __init__(self) -> None:
        self.set_transactions()
        self.set_chain()
        self.set_nodes()

    def set_nodes(self):
        self.nodes = set()

    def set_transactions(self):
        self.transations = []

    def set_chain(self):
        self.chain = self.db.get_doc_list('blockchain')
        if len(self.chain) == 0:
            self.create_genesis()
    
    def create_genesis(self):
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()), 
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transations
        }
        self.transations = []
        id = len(self.chain) + 1
        self.db.add_json_obj(block, 'blockchain', str(id))
        self.set_chain()
        return block, id

    def add_transaction(self, sender, receiver, amount):
        self.transations.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address):
        parse_url = urlparse(address)
        self.nodes.add(parse_url.netloc)
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            dproof = new_proof**2 - previous_proof**2
            hash_operation = self.crypto.generate_hash(str(dproof))
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True)
        return self.crypto.generate_hash(encoded_block)
    
    def is_chain_valid(self, chain):
        if len(chain) in (1,2):
            return True

        previous_block = chain[1]
        block_index = 2
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            dproof = proof**2 - previous_proof**2
            hash_operation = self.crypto.generate_hash(str(dproof))
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = max(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False