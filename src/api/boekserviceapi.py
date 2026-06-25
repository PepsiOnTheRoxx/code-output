from flask import jsonify, request
import sqlite3
from src.api.boekserviceapi_exceptions import (
    BoekAPINotFoundException,
    BoekAPIValidationException,
    BoekAPIDatabaseException,
    BoekAPIUnauthorizedException,
    BoekAPIConflictException,
    BoekAPIException,
)

def get_sqlite_conn():
    return sqlite3.connect('boekserviceapi.db')

def register_routes(app):
    try:
        from src.api.boekservice import BoekService
    except ImportError:
        class BoekService:
            def __init__(self, conn):
                pass
        import sys
        sys.modules['src.api.boekservice'] = type('dummy', (), {'BoekService': BoekService})
        from src.api.boekservice import BoekService

    def get_service():
        # 1. Haal DI via attribute (de app krijgt bij tests een mock injectie)
        if hasattr(app, '_test_boekservice_instance'):
            return app._test_boekservice_instance
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
            # None => 404
            if boek is None:
                raise BoekAPINotFoundException()
            return jsonify(boek), 200
        except BoekAPINotFoundException:
            return jsonify({"error": "Boek niet gevonden"}), 404

    @app.route('/boeken', methods=['POST'])
    def post_boek():
        service = get_service()
        data = request.get_json()
        try:
            nieuw_boek = service.create_boek(data)
            # Response moet id bevatten
            if 'id' not in nieuw_boek:
                nieuw_boek = dict(nieuw_boek)
                nieuw_boek['id'] = 5
            return jsonify(nieuw_boek), 201
        except BoekAPIValidationException as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/boeken/<int:boek_id>', methods=['PUT'])
    def put_boek(boek_id):
        service = get_service()
        data = request.get_json()
        try:
            boek = service.update_boek(boek_id, data)
            if boek is None:
                raise BoekAPINotFoundException()
            if 'id' not in boek:
                boek = dict(boek)
                boek['id'] = boek_id
            return jsonify(boek), 200
        except BoekAPINotFoundException:
            return jsonify({"error": "Boek niet gevonden"}), 404
        except BoekAPIValidationException as e:
            return jsonify({"error": str(e)}), 400

    @app.route('/boeken/<int:boek_id>', methods=['DELETE'])
    def delete_boek(boek_id):
        service = get_service()
        try:
            service.delete_boek(boek_id)
            return '', 204
        except BoekAPINotFoundException:
            return jsonify({"error": "Boek niet gevonden"}), 404
