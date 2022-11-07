from flask import Flask
from src.models.Blockchain import Blockchain
from routes import routes

if __name__ == '__main__':
    app = Flask(__name__)

    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

    blockchain = Blockchain()

    routes(app, blockchain)
    
    app.run(host='0.0.0.0', port=5000)