from flask import Blueprint, jsonify, request
import sqlite3
from src.api.boekserviceapi_exceptions import (
    BoekAPIException,
    BoekAPINotFoundException,
    BoekAPIValidationException,
)

# Exception aliases for compatibility with tests
BoekNotFoundException = BoekAPINotFoundException
InvalidBoekDataException = BoekAPIValidationException

# Concrete BoekService for real CRUD
class BoekService:
    def __init__(self, conn):
        self.conn = conn
        self._ensure_tables()
    def _ensure_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS boeken (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            titel TEXT NOT NULL
        )''')
        self.conn.commit()
    def get_boek(self, boek_id):
        c = self.conn.cursor()
        c.execute("SELECT id, titel FROM boeken WHERE id = ?", (boek_id,))
        row = c.fetchone()
        if row is None:
            raise BoekNotFoundException("Boek niet gevonden")
        return {"id": row[0], "titel": row[1]}
    def create_boek(self, data):
        titel = data.get("titel")
        if not titel:
            raise InvalidBoekDataException("Titel ontbreekt")
        c = self.conn.cursor()
        c.execute("INSERT INTO boeken (titel) VALUES (?)", (titel,))
        self.conn.commit()
        boek_id = c.lastrowid
        return self.get_boek(boek_id)
    def update_boek(self, boek_id, data):
        titel = data.get("titel")
        if not titel:
            raise InvalidBoekDataException("Titel ontbreekt")
        c = self.conn.cursor()
        c.execute("SELECT id FROM boeken WHERE id = ?", (boek_id,))
        if c.fetchone() is None:
            raise BoekNotFoundException("Boek niet gevonden")
        c.execute("UPDATE boeken SET titel = ? WHERE id = ?", (titel, boek_id))
        self.conn.commit()
        return self.get_boek(boek_id)
    def delete_boek(self, boek_id):
        c = self.conn.cursor()
        c.execute("SELECT id FROM boeken WHERE id = ?", (boek_id,))
        if c.fetchone() is None:
            raise BoekNotFoundException("Boek niet gevonden")
        c.execute("DELETE FROM boeken WHERE id = ?", (boek_id,))
        self.conn.commit()
    def get_all_boeken(self):
        c = self.conn.cursor()
        c.execute("SELECT id, titel FROM boeken")
        return [{"id": row[0], "titel": row[1]} for row in c.fetchall()]

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
        except InvalidBoekDataException as e:
            return jsonify({'error': str(e)}), 400

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
