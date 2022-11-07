import hashlib

class CryptoUtils:
    
    def __init__(self) -> None:
        pass

    def generate_hash(self, text:str):
        return hashlib.sha256(text.encode()).hexdigest()
    
