from flask import jsonify, request
import sqlite3
from src.api.boekserviceapi_exceptions import BoekNotFoundException
from src.api.boekserviceapi import BoekService  # deze import moet juist zijn voor patching in testen

def register_routes(app):
    def get_service():
        conn = sqlite3.connect('boeken.sqlite')
        return BoekService(conn)

    @app.route('/api/boeken', methods=['GET'])
    def get_boeken():
        service = get_service()
        boeken = service.get_all_boeken()
        return jsonify(boeken), 200

    @app.route('/api/boeken/<int:boek_id>', methods=['GET'])
    def get_boek(boek_id):
        service = get_service()
        try:
            boek = service.get_boek_by_id(boek_id)
            return jsonify(boek), 200
        except BoekNotFoundException:
            return jsonify({'error': 'Boek not found'}), 404

    @app.route('/api/boeken', methods=['POST'])
    def post_boek():
        service = get_service()
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid data'}), 400
        if 'titel' not in data or 'auteur' not in data:
            return jsonify({'error': 'Invalid data'}), 400
        try:
            nieuw_boek = service.create_boek(data)
            return jsonify(nieuw_boek), 201
        except Exception:
            return jsonify({'error': 'Invalid data'}), 400

    @app.route('/api/boeken/<int:boek_id>', methods=['PUT'])
    def put_boek(boek_id):
        service = get_service()
        data = request.get_json()
        if not data or not isinstance(data, dict):
            return jsonify({'error': 'Invalid data'}), 400
        if 'titel' not in data or 'auteur' not in data:
            return jsonify({'error': 'Invalid data'}), 400
        try:
            updated = service.update_boek(boek_id, data)
            return jsonify(updated), 200
        except BoekNotFoundException:
            return jsonify({'error': 'Boek not found'}), 404

    @app.route('/api/boeken/<int:boek_id>', methods=['DELETE'])
    def delete_boek(boek_id):
        service = get_service()
        try:
            service.delete_boek_by_id(boek_id)
            return '', 204
        except BoekNotFoundException:
            return jsonify({'error': 'Boek not found'}), 404