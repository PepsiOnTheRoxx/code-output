from flask import Blueprint, request, jsonify, make_response
from src.api.vernietigingstaakserviceapi_exceptions import (
    VernietigingstaakNotFoundException,
    InvalidVernietigingstaakDataException,
    UnauthorizedAccessException,
)

class VernietigingstaakService:
    def get_vernietigingstaak(self, taak_id): pass
    def create_vernietigingstaak(self, data): pass
    def update_vernietigingstaak(self, taak_id, data): pass
    def delete_vernietigingstaak(self, taak_id): pass

class VernietigingstaakAPI:
    def __init__(self):
        self.service = None  # will be set per route for test compatibility

    def register_routes(self, app):
        bp = Blueprint('vernietigingstaak_api', __name__)

        @bp.before_request
        def inject_service():
            # Patch self.service for mocked class compatibility (for unittest.mock patching)
            if self.service is None:
                # On first request in a test, set an instance of the currently patched class
                from src.api import vernietigingstaakserviceapi
                self.service = vernietigingstaakserviceapi.VernietigingstaakService()

        @bp.route('/vernietigingstaken/<string:taak_id>', methods=['GET'])
        def get_vernietigingstaak(taak_id):
            try:
                result = self.service.get_vernietigingstaak(taak_id)
                return jsonify(result), 200
            except VernietigingstaakNotFoundException:
                return jsonify({"error": "Vernietigingstaak niet gevonden"}), 404

        @bp.route('/vernietigingstaken', methods=['POST'])
        def create_vernietigingstaak():
            try:
                data = request.get_json(force=True)
                result = self.service.create_vernietigingstaak(data)
                return jsonify(result), 201
            except InvalidVernietigingstaakDataException:
                return jsonify({"error": "Ongeldige vernietigingstaak data"}), 400

        @bp.route('/vernietigingstaken/<string:taak_id>', methods=['PUT'])
        def update_vernietigingstaak(taak_id):
            try:
                data = request.get_json(force=True)
                result = self.service.update_vernietigingstaak(taak_id, data)
                return jsonify(result), 200
            except VernietigingstaakNotFoundException:
                return jsonify({"error": "Vernietigingstaak niet gevonden"}), 404

        @bp.route('/vernietigingstaken/<string:taak_id>', methods=['DELETE'])
        def delete_vernietigingstaak(taak_id):
            try:
                self.service.delete_vernietigingstaak(taak_id)
                return '', 204
            except UnauthorizedAccessException:
                return jsonify({"error": "Geen toegang tot deze taak"}), 403

        app.register_blueprint(bp)
