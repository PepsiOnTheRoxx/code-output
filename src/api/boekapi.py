from flask import request, jsonify
import sqlite3
from src.api.boekapi_exceptions import BoekAPINotFoundException as BoekNotFoundException, BoekAPIValidationException as BoekValidationException

class BoekService:
    def __init__(self, conn):
        self.conn = conn

    def create_boek(self, data):
        if not data.get('titel'):
            raise BoekValidationException('Titel ontbreekt')
        if not data.get('auteur'):
            raise BoekValidationException('Auteur ontbreekt')
        cur = self.conn.cursor()
        cur.execute("INSERT INTO boeken (titel, auteur) VALUES (?, ?)", (data['titel'], data['auteur']))
        self.conn.commit()
        boek_id = cur.lastrowid
        return {"id": boek_id, "titel": data['titel'], "auteur": data['auteur']}

    def get_boek(self, boek_id):
        cur = self.conn.cursor()
        cur.execute("SELECT rowid, * FROM boeken WHERE rowid = ?", (boek_id,))
        row = cur.fetchone()
        if row is None:
            raise BoekNotFoundException("Niet gevonden")
        # Het resultaat van fetchone is nu een Row-object of tuple
        # met rowid vooraan (dus row[0] is id), dan de rest
        # Omdat we row_factory instellen is row["rowid"] beschikbaar
        return {"id": row["rowid"], "titel": row["titel"], "auteur": row["auteur"]}

    def update_boek(self, boek_id, data):
        if not data.get('titel') or not data.get('auteur'):
            raise BoekValidationException('Foutieve data')
        cur = self.conn.cursor()
        cur.execute("SELECT rowid FROM boeken WHERE rowid = ?", (boek_id,))
        if cur.fetchone() is None:
            raise BoekNotFoundException("Niet gevonden")
        cur.execute("UPDATE boeken SET titel = ?, auteur = ? WHERE rowid = ?", (data['titel'], data['auteur'], boek_id))
        self.conn.commit()
        return {"id": boek_id, "titel": data['titel'], "auteur": data['auteur']}

    def delete_boek(self, boek_id):
        cur = self.conn.cursor()
        cur.execute("SELECT rowid FROM boeken WHERE rowid = ?", (boek_id,))
        if cur.fetchone() is None:
            raise BoekNotFoundException("Niet gevonden")
        cur.execute("DELETE FROM boeken WHERE rowid = ?", (boek_id,))
        self.conn.commit()

    def list_boeken(self):
        cur = self.conn.cursor()
        cur.execute("SELECT rowid, * FROM boeken")
        rows = cur.fetchall()
        return [{"id": row["rowid"], "titel": row["titel"], "auteur": row["auteur"]} for row in rows]

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
