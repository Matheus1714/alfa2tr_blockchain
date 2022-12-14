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

    def get_document(self, collection_name:str, document_name:str):
        db = firestore.client()
        doc_ref = db.collection(collection_name).document(document_name)
        doc = doc_ref.get()
        
        if doc.exists:
            return doc.to_dict()
        return {}
    
    def get_doc_list(self, collection_name):
        db = firestore.client()
        coll_ref = db.collection(collection_name)
        docs = coll_ref.stream()
        doc_list = []
        for doc in docs:
            doc_list.append(doc.to_dict())
        return doc_list


