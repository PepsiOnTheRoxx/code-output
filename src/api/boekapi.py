from flask import Blueprint, request, jsonify
from src.api.boekapi_exceptions import (
    BoekNotFoundException,
    BoekValidationException,
)

def create_boek_blueprint(service=None):
    boek_blueprint = Blueprint("boek", __name__)

    if service is None:
        import sqlite3
        from src.api.boekservice import BoekService
        db_conn = sqlite3.connect("boeken.db", check_same_thread=False)
        service = BoekService(db_conn)

    @boek_blueprint.route("/boeken", methods=["GET"])
    def get_all_boeken():
        boeken = service.get_all_boeken()
        return jsonify(boeken), 200

    @boek_blueprint.route("/boeken/<int:boek_id>", methods=["GET"])
    def get_boek_by_id(boek_id):
        try:
            boek = service.get_boek_by_id(boek_id)
            return jsonify(boek), 200
        except BoekNotFoundException:
            return jsonify({"message": "Boek not found"}), 404

    @boek_blueprint.route("/boeken", methods=["POST"])
    def create_boek():
        data = request.get_json()
        try:
            boek = service.create_boek(data)
            return jsonify(boek), 201
        except BoekValidationException as e:
            return jsonify({"message": str(e)}), 400

    @boek_blueprint.route("/boeken/<int:boek_id>", methods=["PUT"])
    def update_boek(boek_id):
        data = request.get_json()
        try:
            boek = service.update_boek(boek_id, data)
            return jsonify(boek), 200
        except BoekNotFoundException:
            return jsonify({"message": "Boek not found"}), 404
        except BoekValidationException as e:
            return jsonify({"message": str(e)}), 400

    @boek_blueprint.route("/boeken/<int:boek_id>", methods=["DELETE"])
    def delete_boek(boek_id):
        try:
            service.delete_boek(boek_id)
            return "", 204
        except BoekNotFoundException:
            return jsonify({"message": "Boek not found"}), 404

    return boek_blueprint

def register_routes(app, service=None):
    # Nu wordt elke keer een nieuwe blueprint met nieuwe routes aangemaakt!
    app.register_blueprint(create_boek_blueprint(service=service))
