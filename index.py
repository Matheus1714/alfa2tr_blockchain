from flask import Flask
from src.models.Blockchain import Blockchain
from routes import routes
from uuid import uuid4

app = Flask(__name__)

# node_address = str(uuid4()).replace('-', '')

# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# blockchain = Blockchain()

# routes(app, blockchain, node_address)

# app.run(host='0.0.0.0', port=5000, debug=True, use_debugger=False, use_reloader=False)

@app.route('/')
def home():
    return 'Home Page Route'


@app.route('/about')
def about():
    return 'About Page Route'


@app.route('/portfolio')
def portfolio():
    return 'Portfolio Page Route'


@app.route('/contact')
def contact():
    return 'Contact Page Route'


@app.route('/api')
def api():
    with open('data.json', mode='r') as my_file:
        text = my_file.read()
        return text