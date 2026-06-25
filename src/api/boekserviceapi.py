from flask import Blueprint, jsonify, request
import sqlite3
from src.api.boekserviceapi_exceptions import (
    BoekNotFoundException,
    InvalidBoekDataException,
)
from src.api.boekserviceapi import BoekService

def register_routes(app):
    bp = Blueprint("boekserviceapi", __name__)

    def get_db_connection():
        conn = sqlite3.connect(":memory:")
        conn.row_factory = sqlite3.Row
        return conn

    @bp.route("/boeken/<int:boek_id>", methods=["GET"])
    def get_boek(boek_id):
        conn = get_db_connection()
        service = BoekService(conn)
        try:
            boek = service.get_boek(boek_id)
            return jsonify(boek), 200
        except BoekNotFoundException:
            return jsonify({'error': 'Boek niet gevonden'}), 404

    @bp.route("/boeken", methods=["POST"])
    def create_boek():
        conn = get_db_connection()
        service = BoekService(conn)
        data = request.get_json()
        try:
            boek = service.create_boek(data)
            return jsonify(boek), 201
        except InvalidBoekDataException as e:
            return jsonify({'error': str(e)}), 400

    @bp.route("/boeken/<int:boek_id>", methods=["PUT"])
    def update_boek(boek_id):
        conn = get_db_connection()
        service = BoekService(conn)
        data = request.get_json()
        try:
            boek = service.update_boek(boek_id, data)
            return jsonify(boek), 200
        except BoekNotFoundException:
            return jsonify({'error': 'Boek niet gevonden'}), 404

    @bp.route("/boeken/<int:boek_id>", methods=["DELETE"])
    def delete_boek(boek_id):
        conn = get_db_connection()
        service = BoekService(conn)
        try:
            service.delete_boek(boek_id)
            return "", 204
        except BoekNotFoundException:
            return jsonify({'error': 'Boek niet gevonden'}), 404

    @bp.route("/boeken", methods=["GET"])
    def get_all_boeken():
        conn = get_db_connection()
        service = BoekService(conn)
        boeken = service.get_all_boeken()
        return jsonify(boeken), 200

    app.register_blueprint(bp)