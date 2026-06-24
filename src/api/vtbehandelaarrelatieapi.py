from flask import request, jsonify
from src.api.vtbehandelaarrelatieapi_exceptions import (
    VTBehandelaarRelatieNotFound,
    VTBehandelaarRelatieInvalidData,
)

class VTBehandelaarRelatieAPI:
    _relaties = {}
    _next_id = 1

    def register_routes(self, app):
        @app.route("/behandelaarrelatie/<int:id>", methods=["GET"])
        def get_behandelaarrelatie_route(id):
            try:
                result = self.get_behandelaarrelatie(id)
                return jsonify(result), 200
            except VTBehandelaarRelatieNotFound:
                return '', 404

        @app.route("/behandelaarrelatie", methods=["POST"])
        def create_behandelaarrelatie_route():
            try:
                data = request.get_json()
                result = self.create_behandelaarrelatie(data)
                return jsonify(result), 201
            except VTBehandelaarRelatieInvalidData:
                return '', 400

        @app.route("/behandelaarrelatie/<int:id>", methods=["PUT"])
        def update_behandelaarrelatie_route(id):
            try:
                data = request.get_json()
                result = self.update_behandelaarrelatie(id, data)
                return jsonify(result), 200
            except VTBehandelaarRelatieNotFound:
                return '', 404

        @app.route("/behandelaarrelatie/<int:id>", methods=["DELETE"])
        def delete_behandelaarrelatie_route(id):
            try:
                self.delete_behandelaarrelatie(id)
                return '', 204
            except VTBehandelaarRelatieNotFound:
                return '', 404

    def get_behandelaarrelatie(self, id):
        if id in self._relaties:
            return {"id": id, "naam": self._relaties[id]["naam"]}
        raise VTBehandelaarRelatieNotFound(f"Behandelaar relatie {id} niet gevonden")

    def create_behandelaarrelatie(self, data):
        if not data or not isinstance(data, dict) or not data.get('naam'):
            raise VTBehandelaarRelatieInvalidData("Naam is verplicht")
        new_id = self._next_id
        self._relaties[new_id] = {"naam": data["naam"]}
        self._next_id += 1
        return {"id": new_id, "naam": data["naam"]}

    def update_behandelaarrelatie(self, id, data):
        if id not in self._relaties:
            raise VTBehandelaarRelatieNotFound(f"Behandelaar relatie {id} niet gevonden")
        if not data or not isinstance(data, dict) or not data.get('naam'):
            raise VTBehandelaarRelatieInvalidData("Naam is verplicht")
        self._relaties[id]["naam"] = data["naam"]
        return {"id": id, "naam": data["naam"]}

    def delete_behandelaarrelatie(self, id):
        if id not in self._relaties:
            raise VTBehandelaarRelatieNotFound(f"Behandelaar relatie {id} niet gevonden")
        del self._relaties[id]
