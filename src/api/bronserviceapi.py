from flask import request, jsonify
from src.api.bronserviceapi_exceptions import (
    BronNotFoundException,
    BronAlreadyExistsException,
)

# Dummy in-memory storage for demonstration
_bron_store = {}
_next_id = [1]  # mutable, to allow increment

class BronService:
    def get_bron(self, bron_id):
        bron = _bron_store.get(bron_id)
        if not bron:
            raise BronNotFoundException(f"Bron met id {bron_id} niet gevonden")
        return bron

    def create_bron(self, bron_data):
        # For demo: check for uniqueness on 'name'
        for bron in _bron_store.values():
            if 'name' in bron_data and bron['name'] == bron_data['name']:
                raise BronAlreadyExistsException("Already exists")
        bron_id = _next_id[0]
        _next_id[0] += 1
        bron = {'bron_id': bron_id, **bron_data}
        _bron_store[bron_id] = bron
        return bron

    def update_bron(self, bron_id, bron_data):
        if bron_id not in _bron_store:
            raise BronNotFoundException("Not found")
        _bron_store[bron_id].update(bron_data)
        _bron_store[bron_id]['bron_id'] = bron_id  # always include bron_id
        return _bron_store[bron_id]

    def delete_bron(self, bron_id):
        if bron_id not in _bron_store:
            raise BronNotFoundException("Bron niet gevonden")
        del _bron_store[bron_id]

def register_routes(app):
    @app.route('/bron/<int:bron_id>', methods=['GET'])
    def get_bron(bron_id):
        service = BronService()
        try:
            result = service.get_bron(bron_id)
            return jsonify(result), 200
        except BronNotFoundException as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/bron', methods=['POST'])
    def create_bron():
        service = BronService()
        data = request.get_json()
        try:
            result = service.create_bron(data)
            return jsonify(result), 201
        except BronAlreadyExistsException as e:
            return jsonify({'error': str(e)}), 409

    @app.route('/bron/<int:bron_id>', methods=['PUT'])
    def update_bron(bron_id):
        service = BronService()
        data = request.get_json()
        try:
            result = service.update_bron(bron_id, data)
            return jsonify(result), 200
        except BronNotFoundException as e:
            return jsonify({'error': str(e)}), 404

    @app.route('/bron/<int:bron_id>', methods=['DELETE'])
    def delete_bron(bron_id):
        service = BronService()
        try:
            service.delete_bron(bron_id)
            return '', 204
        except BronNotFoundException as e:
            return jsonify({'error': str(e)}), 404
