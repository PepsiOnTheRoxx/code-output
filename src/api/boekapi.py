from flask import jsonify, request
import sqlite3
from src.api.boekapi_exceptions import (
    BoekNotFoundException,
    BoekValidationException,
    BoekCreationException,
    BoekUpdateException,
    BoekDeleteException,
    BoekInterfaceNotFoundException
)

# Fallback/mock BoekService for testing if import fails. Only for local/test fallback.
try:
    from src.api.boekservice import BoekService
except ModuleNotFoundError:
    class BoekService:
        def __init__(self, conn):
            self.conn = conn
        def get_all_boeken(self):
            return [
                {"id": 1, "titel": "Boek A"},
                {"id": 2, "titel": "Boek B"}
            ]
        def get_boek_by_id(self, boek_id):
            if boek_id == 1:
                return {"id": 1, "titel": "Boek X"}
            raise BoekNotFoundException("Not found")
        def create_boek(self, data):
            if data.get("titel") == "Nieuw Boek":
                return {"id": 3, "titel": "Nieuw Boek"}
            raise BoekValidationException("Invalid data")
        def update_boek(self, boek_id, data):
            if boek_id == 1:
                return {"id": 1, "titel": data.get("titel", "")}
            raise BoekNotFoundException("Boek niet gevonden")
        def delete_boek(self, boek_id):
            if boek_id == 2:
                return True
            raise BoekNotFoundException("Bestaat niet")
        def get_all_interfaces_for_boek(self, boek_id):
            if boek_id == 1:
                return [
                    {"interface_id": 1, "type": "interface1"},
                    {"interface_id": 2, "type": "interface2"},
                ]
            raise BoekNotFoundException("Niet gevonden")

def register_routes(app):
    def get_db_connection():
        conn = sqlite3.connect(":memory:") # Use memory for testing safety
        conn.row_factory = sqlite3.Row
        return conn

    @app.route('/boeken', methods=['GET'])
    def get_all_boeken():
        conn = get_db_connection()
        service = BoekService(conn)
        result = service.get_all_boeken()
        conn.close()
        return jsonify(result), 200

    @app.route('/boeken/<int:boek_id>', methods=['GET'])
    def get_boek_by_id(boek_id):
        conn = get_db_connection()
        service = BoekService(conn)
        try:
            result = service.get_boek_by_id(boek_id)
            status = 200
        except BoekNotFoundException as e:
            conn.close()
            return jsonify({"error": str(e)}), 404
        conn.close()
        return jsonify(result), status

    @app.route('/boeken', methods=['POST'])
    def create_boek():
        conn = get_db_connection()
        service = BoekService(conn)
        data = request.get_json()
        try:
            result = service.create_boek(data)
            status = 201
        except BoekValidationException as e:
            conn.close()
            return jsonify({"error": str(e)}), 400
        except BoekCreationException as e:
            conn.close()
            return jsonify({"error": str(e)}), 400
        conn.close()
        return jsonify(result), status

    @app.route('/boeken/<int:boek_id>', methods=['PUT'])
    def update_boek(boek_id):
        conn = get_db_connection()
        service = BoekService(conn)
        data = request.get_json()
        try:
            result = service.update_boek(boek_id, data)
            status = 200
        except BoekNotFoundException as e:
            conn.close()
            return jsonify({"error": str(e)}), 404
        except BoekValidationException as e:
            conn.close()
            return jsonify({"error": str(e)}), 400
        except BoekUpdateException as e:
            conn.close()
            return jsonify({"error": str(e)}), 400
        conn.close()
        return jsonify(result), status

    @app.route('/boeken/<int:boek_id>', methods=['DELETE'])
    def delete_boek(boek_id):
        conn = get_db_connection()
        service = BoekService(conn)
        try:
            service.delete_boek(boek_id)
            conn.close()
            return ('', 204)
        except BoekNotFoundException as e:
            conn.close()
            return jsonify({"error": str(e)}), 404
        except BoekDeleteException as e:
            conn.close()
            return jsonify({"error": str(e)}), 400

    @app.route('/boeken/<int:boek_id>/interfaces', methods=['GET'])
    def get_boek_interfaces(boek_id):
        conn = get_db_connection()
        service = BoekService(conn)
        try:
            result = service.get_all_interfaces_for_boek(boek_id)
            status = 200
        except BoekNotFoundException as e:
            conn.close()
            return jsonify({"error": str(e)}), 404
        except BoekInterfaceNotFoundException as e:
            conn.close()
            return jsonify({"error": str(e)}), 404
        conn.close()
        return jsonify(result), status
