from flask import request, jsonify

from src.api.vtbronnenrelatieapi_exceptions import (
    VTBronnenRelatieNotFoundException,
    VTBronnenRelatieValidationException,
)

class VTBronnenRelatieAPI:
    def register_routes(self, app):
        @app.route('/vtbronnenrelatie', methods=['GET'])
        def get_all_relaties_route():
            try:
                return jsonify(self.get_all_relaties()), 200
            except Exception as ex:
                return jsonify({'error': str(ex)}), 500

        @app.route('/vtbronnenrelatie/<int:relatie_id>', methods=['GET'])
        def get_relatie_route(relatie_id):
            try:
                return jsonify(self.get_relatie_by_id(relatie_id)), 200
            except VTBronnenRelatieNotFoundException as ex:
                return jsonify({'error': str(ex)}), 404
            except Exception as ex:
                return jsonify({'error': str(ex)}), 500

        @app.route('/vtbronnenrelatie', methods=['POST'])
        def post_relatie_route():
            try:
                data = request.json
                return jsonify(self.create_relatie(data)), 201
            except VTBronnenRelatieValidationException as ex:
                return jsonify({'error': str(ex)}), 400
            except Exception as ex:
                return jsonify({'error': str(ex)}), 500

        @app.route('/vtbronnenrelatie/<int:relatie_id>', methods=['PUT'])
        def put_relatie_route(relatie_id):
            try:
                data = request.json
                return jsonify(self.update_relatie(relatie_id, data)), 200
            except VTBronnenRelatieNotFoundException as ex:
                return jsonify({'error': str(ex)}), 404
            except VTBronnenRelatieValidationException as ex:
                return jsonify({'error': str(ex)}), 400
            except Exception as ex:
                return jsonify({'error': str(ex)}), 500

        @app.route('/vtbronnenrelatie/<int:relatie_id>', methods=['DELETE'])
        def delete_relatie_route(relatie_id):
            try:
                self.delete_relatie(relatie_id)
                return '', 204
            except VTBronnenRelatieNotFoundException as ex:
                return jsonify({'error': str(ex)}), 404
            except Exception as ex:
                return jsonify({'error': str(ex)}), 500

    def get_all_relaties(self):
        # Implementatie hier (mock/voorbeeld)
        return []

    def get_relatie_by_id(self, relatie_id):
        # Implementatie hier (mock/voorbeeld)
        raise VTBronnenRelatieNotFoundException("Not implemented")

    def create_relatie(self, data):
        # Implementatie hier (mock/voorbeeld)
        raise VTBronnenRelatieValidationException("Not implemented")

    def update_relatie(self, relatie_id, data):
        # Implementatie hier (mock/voorbeeld)
        raise VTBronnenRelatieNotFoundException("Not implemented")

    def delete_relatie(self, relatie_id):
        # Implementatie hier (mock/voorbeeld)
        raise VTBronnenRelatieNotFoundException("Not implemented")
