from flask import request, jsonify
from src.api.bronserviceapi_exceptions import (
    BronNotFoundException,
    BronAlreadyExistsException,
)
  
class BronService:
    def get_bron(self, bron_id):
        raise NotImplementedError

    def create_bron(self, bron_data):
        raise NotImplementedError

    def update_bron(self, bron_id, bron_data):
        raise NotImplementedError

    def delete_bron(self, bron_id):
        raise NotImplementedError

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
