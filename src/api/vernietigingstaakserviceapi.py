from flask import Blueprint, request, jsonify
from src.api.vernietigingstaakserviceapi_exceptions import (
    VernietigingstaakNotFoundException,
    InvalidVernietigingstaakDataException,
    UnauthorizedAccessException,
)

class VernietigingstaakService:
    def __init__(self):
        # Simuleer eenvoudige in-memory opslag voor taken
        if not hasattr(self, '_storage'):
            self._storage = {}

    def get_vernietigingstaak(self, taak_id):
        if taak_id not in self._storage:
            raise VernietigingstaakNotFoundException()
        return self._storage[taak_id]

    def create_vernietigingstaak(self, data):
        if not isinstance(data, dict) or 'document_id' not in data:
            raise InvalidVernietigingstaakDataException()
        # Simuleer een nieuwe id aanmaken
        new_id = f"vt-{len(self._storage) + 1}"
        taak = {
            "id": new_id,
            "document_id": data["document_id"],
            "status": "aangevraagd"
        }
        self._storage[new_id] = taak
        return taak

    def update_vernietigingstaak(self, taak_id, data):
        if taak_id not in self._storage:
            raise VernietigingstaakNotFoundException()
        # Alleen status mag aangepast woorden voor eenvoud
        taak = self._storage[taak_id]
        if "status" in data:
            taak["status"] = data["status"]
        self._storage[taak_id] = taak
        return taak

    def delete_vernietigingstaak(self, taak_id):
        # Simuleer dat je sommige taken niet mag verwijderen
        if taak_id == "vt-unauth":
            raise UnauthorizedAccessException()
        self._storage.pop(taak_id, None)

class VernietigingstaakAPI:
    def __init__(self):
        self.service = None  # will be set per route for test compatibility

    def register_routes(self, app):
        bp = Blueprint('vernietigingstaak_api', __name__)

        @bp.before_request
        def inject_service():
            if self.service is None:
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
