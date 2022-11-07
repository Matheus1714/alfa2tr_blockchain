from datetime import datetime
import json

from src.utils.CryptoUtils import CryptoUtils
from src.db.Firestore import Firestore

class Blockchain:

    cryoto = CryptoUtils()
    db = Firestore()

    def __init__(self) -> None:
        self.set_chain()

    def create_genesis(self):
        self.create_block(proof=1, previous_hash='0')

    def set_chain(self):
        self.chain = self.db.get_doc_list('blockchain')
        if len(self.chain) == 0:
            self.create_genesis()

    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash
        }
        id = self.cryoto.generate_key()
        self.db.add_json_obj(block, 'blockchain', id)
        self.set_chain()
        return block, id
    
    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            dproof = new_proof**2 - previous_proof**2
            hash_operation = self.cryoto.generate_hash(str(dproof))
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True)
        return self.cryoto.generate_hash(encoded_block)
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            dproof = proof**2 - previous_proof**2
            hash_operation = self.cryoto.generate_hash(str(dproof))
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    