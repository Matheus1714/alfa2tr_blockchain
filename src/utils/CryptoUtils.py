import hashlib
from uuid import uuid4

class CryptoUtils:
    
    def __init__(self) -> None:
        pass

    def generate_hash(self, text:str):
        return hashlib.sha256(text.encode()).hexdigest()
    
    def generate_key(self):
        rand_token = uuid4()
        return rand_token.hex
    
