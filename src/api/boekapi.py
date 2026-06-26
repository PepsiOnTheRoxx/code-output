from flask import request, jsonify
import sqlite3
from src.api.boekapi_exceptions import BoekNotFoundException, BoekValidationException

class BoekService:
    def __init__(self, conn):
        self.conn = conn

    def create_boek(self, data):
        raise NotImplementedError()

    def get_boek(self, boek_id):
        raise NotImplementedError()

    def update_boek(self, boek_id, data):
        raise NotImplementedError()

    def delete_boek(self, boek_id):
        raise NotImplementedError()

    def list_boeken(self):
        raise NotImplementedError()

def register_routes(app):
    def get_service():
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        return BoekService(conn)

    @app.route("/boeken", methods=["POST"])
    def create_boek():
        service = get_service()
        data = request.get_json(force=True)
        try:
            boek = service.create_boek(data)
            return jsonify(boek), 201
        except BoekValidationException as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/boeken/<int:boek_id>", methods=["GET"])
    def read_boek(boek_id):
        service = get_service()
        try:
            boek = service.get_boek(boek_id)
            return jsonify(boek), 200
        except BoekNotFoundException as e:
            return jsonify({"error": str(e)}), 404

    @app.route("/boeken/<int:boek_id>", methods=["PUT"])
    def update_boek(boek_id):
        service = get_service()
        data = request.get_json(force=True)
        try:
            boek = service.update_boek(boek_id, data)
            return jsonify(boek), 200
        except BoekNotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except BoekValidationException as e:
            return jsonify({"error": str(e)}), 400

    @app.route("/boeken/<int:boek_id>", methods=["DELETE"])
    def delete_boek(boek_id):
        service = get_service()
        try:
            service.delete_boek(boek_id)
            return "", 204
        except BoekNotFoundException as e:
            return jsonify({"error": str(e)}), 404

    @app.route("/boeken", methods=["GET"])
    def list_boeken():
        service = get_service()
        boeken = service.list_boeken()
        return jsonify(boeken), 200