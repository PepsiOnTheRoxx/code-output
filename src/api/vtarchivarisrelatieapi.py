from flask import Flask, request, jsonify
from src.api.vtarchivarisrelatieapi_exceptions import (
    VTArchivarisRelatieAPINotFound,
    VTArchivarisRelatieAPIInvalidInput,
    VTArchivarisRelatieAPIException,
)

_vtarchivarisrelaties = {}
_next_id = 1

def reset_vtarchivarisrelaties():
    global _vtarchivarisrelaties, _next_id
    _vtarchivarisrelaties = {}
    _next_id = 1

def get_vtarchivarisrelatie(relatie_id: int):
    relatie = _vtarchivarisrelaties.get(relatie_id)
    if not relatie:
        raise VTArchivarisRelatieAPINotFound()
    return relatie.copy()

def create_vtarchivarisrelatie(data):
    global _next_id
    naam = data.get("naam")
    if not naam or not isinstance(naam, str) or not naam.strip():
        raise VTArchivarisRelatieAPIInvalidInput()
    relatie = {"id": _next_id, "naam": naam}
    _vtarchivarisrelaties[_next_id] = relatie
    _next_id += 1
    return relatie.copy()

def update_vtarchivarisrelatie(relatie_id: int, data):
    if relatie_id not in _vtarchivarisrelaties:
        raise VTArchivarisRelatieAPINotFound()
    naam = data.get("naam")
    if not naam or not isinstance(naam, str) or not naam.strip():
        raise VTArchivarisRelatieAPIInvalidInput()
    _vtarchivarisrelaties[relatie_id]["naam"] = naam
    return _vtarchivarisrelaties[relatie_id].copy()

def delete_vtarchivarisrelatie(relatie_id: int):
    if relatie_id not in _vtarchivarisrelaties:
        raise VTArchivarisRelatieAPINotFound()
    del _vtarchivarisrelaties[relatie_id]
    return None

# REST endpoint exposure
def create_app():
    app = Flask(__name__)

    @app.errorhandler(VTArchivarisRelatieAPINotFound)
    def notfound(e):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(VTArchivarisRelatieAPIInvalidInput)
    def invalid(e):
        return jsonify({"error": "Invalid Input"}), 400

    @app.errorhandler(VTArchivarisRelatieAPIException)
    def generic_exception(e):
        return jsonify({"error": "VTArchivarisRelatieAPI Exception"}), 500

    @app.route("/vtarchivarisrelaties/<int:relatie_id>", methods=["GET"])
    def http_get_vtarchivarisrelatie(relatie_id):
        return jsonify(get_vtarchivarisrelatie(relatie_id))

    @app.route("/vtarchivarisrelaties", methods=["POST"])
    def http_create_vtarchivarisrelatie():
        data = request.get_json(force=True)
        return jsonify(create_vtarchivarisrelatie(data)), 201

    @app.route("/vtarchivarisrelaties/<int:relatie_id>", methods=["PUT"])
    def http_update_vtarchivarisrelatie(relatie_id):
        data = request.get_json(force=True)
        return jsonify(update_vtarchivarisrelatie(relatie_id, data))

    @app.route("/vtarchivarisrelaties/<int:relatie_id>", methods=["DELETE"])
    def http_delete_vtarchivarisrelatie(relatie_id):
        delete_vtarchivarisrelatie(relatie_id)
        return '', 204

    return app
