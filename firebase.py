from src.db.Firestore import Firestore
from src.utils.CryptoUtils import CryptoUtils

firestore = Firestore()
crypto = CryptoUtils()

from datetime import datetime

blockchain = [
    {
        'id':crypto.generate_key(),
        'timestamp': datetime.now(),
        'nonce': 123123,
        'hash': crypto.generate_hash('1'),
        'previous_hash': crypto.generate_hash('0')
    },
    {
        'id':crypto.generate_key(),
        'timestamp': datetime.now(),
        'nonce': 123123,
        'hash': crypto.generate_hash('2'),
        'previous_hash': crypto.generate_hash('1')
    },
    {
        'id':crypto.generate_key(),
        'timestamp': datetime.now(),
        'nonce': 123123,
        'hash': crypto.generate_hash('3'),
        'previous_hash': crypto.generate_hash('2')
    },
    {
        'id':crypto.generate_key(),
        'timestamp': datetime.now(),
        'nonce': 123123,
        'hash': crypto.generate_hash('4'),
        'previous_hash': crypto.generate_hash('3')
    },
]

for block in blockchain:
    firestore.add_json_obj(block, collection_name='blockchain', document_name=crypto.generate_key())