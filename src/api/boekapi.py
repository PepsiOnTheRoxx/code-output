from flask import Blueprint, request, jsonify
import sqlite3
from src.api.boekapi_exceptions import (
    BoekNotFoundException,
    BoekValidationException,
    BoekAPIException,
)
# Stel dat de BoekService deze interface heeft:
# class BoekService:
#     def __init__(self, db_conn): ...
#     def get_all_boeken(self): ...
#     def get_boek_by_id(self, boek_id): ...
#     def create_boek(self, data): ...
#     def update_boek(self, boek_id, data): ...
#     def delete_boek(self, boek_id): ...
from src.api.boekservice import BoekService

boek_blueprint = Blueprint("boek", __name__)

def register_routes(app):
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

    app.register_blueprint(boek_blueprint)