from flask import jsonify, request
import sqlite3
from src.api.boekserviceapi_exceptions import BoekNotFoundException
from src.api.boekserviceapi_exceptions import BoekAPIValidationException, BoekAPIDatabaseException, BoekAPIUnauthorizedException, BoekAPIConflictException
from src.api.boekserviceapi_exceptions import BoekAPIException
from src.api.boekserviceapi import BoekService

def get_sqlite_conn():
    return sqlite3.connect("boekserviceapi.db")

def register_routes(app):
    def get_service():
        return BoekService(get_sqlite_conn())

    @app.route('/boeken', methods=['GET'])
    def get_boeken():
        service = get_service()
        boeken = service.get_all_boeken()
        return jsonify(boeken), 200

    @app.route('/boeken/<int:boek_id>', methods=['GET'])
    def get_boek(boek_id):
        service = get_service()
        try:
            boek = service.get_boek(boek_id)
            return jsonify(boek), 200
        except BoekNotFoundException:
            return jsonify({"error": "Boek niet gevonden"}), 404

    @app.route('/boeken', methods=['POST'])
    def post_boek():
        service = get_service()
        data = request.get_json()
        try:
            nieuw_boek = service.create_boek(data)
            return jsonify(nieuw_boek), 201
        except BoekAPIValidationException as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/boeken/<int:boek_id>', methods=['PUT'])
    def put_boek(boek_id):
        service = get_service()
        data = request.get_json()
        try:
            boek = service.update_boek(boek_id, data)
            return jsonify(boek), 200
        except BoekNotFoundException:
            return jsonify({"error": "Boek niet gevonden"}), 404
        except BoekAPIValidationException as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/boeken/<int:boek_id>', methods=['DELETE'])
    def delete_boek(boek_id):
        service = get_service()
        try:
            service.delete_boek(boek_id)
            return '', 204
        except BoekNotFoundException:
            return jsonify({"error": "Boek niet gevonden"}), 404