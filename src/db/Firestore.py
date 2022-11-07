from firebase_admin import firestore, initialize_app, credentials, firestore
from dotenv import dotenv_values
from pathlib import Path

class Firestore:
    
    def __init__(self)->None:
        self.connect_db()
    
    def get_credentials(self):
        config = dotenv_values(".env")
        SERVICE_ACCOUNT_FIREBASE = config.get('SERVICE_ACCOUNT_FIREBASE')
        return credentials.Certificate(SERVICE_ACCOUNT_FIREBASE)

    def connect_db(self):
        cred = self.get_credentials()
        initialize_app(cred)

    def add_json_obj(self, json_obj:dict, collection_name:str, document_name:str):
        db = firestore.client()
        doc_ref = db.collection(collection_name).document(document_name)
        doc_ref.set(json_obj)
