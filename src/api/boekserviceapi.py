from flask import jsonify, request
import sqlite3
from src.api.boekserviceapi_exceptions import BoekNotFoundException, InvalidBoekDataException
from src.api.boekservice import BoekService

def get_db_connection():
    # Dit is enkel voor demonstratie/test-doeleinden,
    # in productie hoort de connectie elders beheerd te worden
    return sqlite3.connect(':memory:')

def register_routes(app):
    def get_service():
        # Fixture/mock tests vervangen de BoekService tijdens unittests
        return BoekService(get_db_connection())

    @app.route('/boeken', methods=['GET'])
    def get_all_boeken():
        service = get_service()
        boeken = service.get_all_boeken()
        return jsonify(boeken), 200

    @app.route('/boeken/<int:boek_id>', methods=['GET'])
    def get_boek_by_id(boek_id):
        service = get_service()
        try:
            boek = service.get_boek_by_id(boek_id)
            return jsonify(boek), 200
        except BoekNotFoundException as e:
            return jsonify({"error": str(e)}), 404

    @app.route('/boeken', methods=['POST'])
    def create_boek():
        service = get_service()
        data = request.get_json()
        try:
            boek = service.create_boek(data)
            return jsonify(boek), 201
        except InvalidBoekDataException as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/boeken/<int:boek_id>', methods=['PUT'])
    def update_boek(boek_id):
        service = get_service()
        data = request.get_json()
        try:
            boek = service.update_boek(boek_id, data)
            return jsonify(boek), 200
        except BoekNotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except InvalidBoekDataException as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/boeken/<int:boek_id>', methods=['DELETE'])
    def delete_boek(boek_id):
        service = get_service()
        try:
            service.delete_boek(boek_id)
            return '', 204
        except BoekNotFoundException as e:
            return jsonify({"error": str(e)}), 404