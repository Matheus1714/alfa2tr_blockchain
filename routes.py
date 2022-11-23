from flask import jsonify, request
from src.models.Blockchain import Blockchain
from uuid import uuid4

def routes(app, blockchain:Blockchain, node_address):
    
    @app.route('/mine_block', methods = ['GET'])
    def mine_block():
        previous_block = blockchain.get_previous_block()
        previous_proof = previous_block['proof']
        proof = blockchain.proof_of_work(previous_proof)
        previous_hash = blockchain.hash(previous_block)
        blockchain.add_transaction(sender=node_address, receiver='Raspberry PI', amount=200)
        block, id = blockchain.create_block(proof, previous_hash)
        response = {
            'msg':'mine block',
            'index': block['index'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
            'transactions': block['transactions']
        }
        return jsonify(response, indent=2, sort_keys=False), 200

    @app.route('/get_chain', methods = ['GET'])
    def get_chain():
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
        return jsonify(response, indent=2, sort_keys=False), 200

    @app.route('/is_valid', methods = ['GET'])
    def is_valid():
        chain = sorted(blockchain.chain, key = lambda x: x['index'])
        is_valid = blockchain.is_chain_valid(chain)
        if is_valid:
            response = {
                'msg': 'blockchain is valid'
            }
        else:
            response = {
                'msg': 'blockchain invalid'
            }
        
        return jsonify(response, indent=2, sort_keys=False), 200
    
    @app.route('/add_transaction', methods = ['POST'])
    def add_transaction():
        transaction = request.get_json()
        transaction_keys = ['sender', 'receiver', 'amount']
        if not all(key in transaction for key in transaction_keys):
            response = {
                'msg': 'Some elements are missing'
            }
            return jsonify(response, indent=2, sort_keys=False), 400
        index = blockchain.add_transaction(**transaction)
        response = {
            'msg': f'created transaction in block {index}',
        }
        return jsonify(response, indent=2, sort_keys=False), 201
    
    @app.route('/connect_node', methods = ['POST'])
    def connect_node():
        json = request.get_json()
        nodes = json.get('nodes')
        if nodes is None:
            response = {
                'msg': 'empty nodes'
            }
            return jsonify(response, indent=2, sort_keys=False), 400
        for node in nodes:
            blockchain.add_node(node)
        response = {
            'msg': 'all nodes connecteds',
            'total_nodes': list(blockchain.nodes)
        }
        return jsonify(response, indent=2, sort_keys=False), 201

    @app.route('/replace_chain', methods=['GET'])
    def replace_chain():
        is_chain_replaced = blockchain.replace_chain()
        if is_chain_replaced:
            response = {
                'msg': 'new replace',
                'new_chain': blockchain.chain
            }
        else:
            response = {
                'msg': 'not replaced',
                'actual_chain': blockchain.chain
            }
        return jsonify(response, indent=2, sort_keys=False), 201
    
    @app.route('/collect_audio', methods=['GET'])
    def collect_audio():
        
        response = {
            "msg": "get audio sucess"
        }

        return jsonify(response, indent=2, sort_keys=False), 200

    @app.route('/get_info/<int:id_aluno>', methods=['GET'])
    def get_info(id_aluno):
        response = {
            "msg": ""
        }
        return jsonify(response, indent=2, sort_keys=False), 200

    @app.route('/', methods=['GET'])
    def homepage():
        response = {
            "msg": "initial page"
        }
        return jsonify(response, indent=2, sort_keys=False), 200


