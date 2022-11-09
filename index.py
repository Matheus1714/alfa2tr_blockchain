from flask import Flask
from src.models.Blockchain import Blockchain
from routes import routes
from uuid import uuid4

app = Flask(__name__)

node_address = str(uuid4()).replace('-', '')

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

blockchain = Blockchain()

routes(app, blockchain, node_address)
# app.run(host='0.0.0.0', port=5000, debug=True, use_debugger=False, use_reloader=False)