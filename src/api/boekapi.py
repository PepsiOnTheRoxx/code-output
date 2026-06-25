from flask import jsonify, request
import sqlite3
from src.api.boekapi_exceptions import BoekNotFoundException, BoekValidationException
from src.services.boek_service import BoekService

def register_routes(app):
    def get_db_connection():
        conn = sqlite3.connect("database.sqlite")
        conn.row_factory = sqlite3.Row
        return conn

    @app.route('/boeken', methods=['GET'])
    def get_boeken():
        conn = get_db_connection()
        service = BoekService(conn)
        boeken = service.get_all_boeken()
        conn.close()
        return jsonify(boeken), 200

    @app.route('/boeken/<int:boek_id>', methods=['GET'])
    def get_boek_by_id(boek_id):
        conn = get_db_connection()
        service = BoekService(conn)
        try:
            boek = service.get_boek_by_id(boek_id)
            conn.close()
            return jsonify(boek), 200
        except BoekNotFoundException:
            conn.close()
            return jsonify({"error": "Boek niet gevonden"}), 404

    @app.route('/boeken', methods=['POST'])
    def create_boek():
        data = request.get_json()
        conn = get_db_connection()
        service = BoekService(conn)
        try:
            created = service.create_boek(data)
            conn.close()
            return jsonify(created), 201
        except BoekValidationException as e:
            conn.close()
            return jsonify({"error": str(e)}), 400

    @app.route('/boeken/<int:boek_id>', methods=['PUT'])
    def update_boek(boek_id):
        data = request.get_json()
        conn = get_db_connection()
        service = BoekService(conn)
        try:
            updated = service.update_boek(boek_id, data)
            conn.close()
            return jsonify(updated), 200
        except BoekNotFoundException:
            conn.close()
            return jsonify({"error": "Boek niet gevonden"}), 404
        except BoekValidationException as e:
            conn.close()
            return jsonify({"error": str(e)}), 400

    @app.route('/boeken/<int:boek_id>', methods=['DELETE'])
    def delete_boek(boek_id):
        conn = get_db_connection()
        service = BoekService(conn)
        try:
            service.delete_boek(boek_id)
            conn.close()
            return '', 204
        except BoekNotFoundException:
            conn.close()
            return jsonify({"error": "Boek niet gevonden"}), 404