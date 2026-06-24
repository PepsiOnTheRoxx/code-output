from flask import request, jsonify
from src.api.vtbehandelaarrelatieapi_exceptions import (
    VTBehandelaarRelatieNotFound,
    VTBehandelaarRelatieInvalidData,
)

class VTBehandelaarRelatieAPI:
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
        raise NotImplementedError

    def create_behandelaarrelatie(self, data):
        raise NotImplementedError

    def update_behandelaarrelatie(self, id, data):
        raise NotImplementedError

    def delete_behandelaarrelatie(self, id):
        raise NotImplementedError