from flask import Flask, jsonify, request
from src.api.vtarchivarisrelatieapi_exceptions import (
    VTArchivarisRelatieNotFound,
    VTArchivarisRelatieValidationError,
)

class VTArchivarisRelatieService:
    def get_relatie(self, relatie_id):
        raise NotImplementedError

    def create_relatie(self, data):
        raise NotImplementedError

    def update_relatie(self, relatie_id, data):
        raise NotImplementedError

    def delete_relatie(self, relatie_id):
        raise NotImplementedError

class VTArchivarisRelatieAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.service = VTArchivarisRelatieService()
        self._configure_routes()
        self._configure_error_handlers()

    def _configure_routes(self):
        @self.app.route('/archivarisrelatie/<int:relatie_id>', methods=['GET'])
        def get_archivarisrelatie(relatie_id):
            result = self.service.get_relatie(relatie_id)
            return jsonify(result), 200

        @self.app.route('/archivarisrelatie', methods=['POST'])
        def post_archivarisrelatie():
            data = request.get_json()
            result = self.service.create_relatie(data)
            return jsonify(result), 201

        @self.app.route('/archivarisrelatie/<int:relatie_id>', methods=['PATCH'])
        def patch_archivarisrelatie(relatie_id):
            data = request.get_json()
            result = self.service.update_relatie(relatie_id, data)
            return jsonify(result), 200

        @self.app.route('/archivarisrelatie/<int:relatie_id>', methods=['DELETE'])
        def delete_archivarisrelatie(relatie_id):
            self.service.delete_relatie(relatie_id)
            return '', 204

    def _configure_error_handlers(self):
        @self.app.errorhandler(VTArchivarisRelatieNotFound)
        def handle_not_found(e):
            return jsonify({'message': str(e)}), 404

        @self.app.errorhandler(VTArchivarisRelatieValidationError)
        def handle_validation_error(e):
            return jsonify({'message': str(e)}), 400