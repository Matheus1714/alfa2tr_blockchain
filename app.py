from flask import Flask
from src.models.Blockchain import BlockChain
from routes import routes

if __name__ == '__main__':
    app = Flask(__name__)

    blockchain = BlockChain()

    routes(app, blockchain)
    
    app.run(host='0.0.0.0', port=5000)