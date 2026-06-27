from flask import jsonify, request
import sqlite3
from src.api.boekapi_exceptions import (
    BoekNotFoundException,
    InvalidBoekDataException,
)

def get_db_connection():
    conn = sqlite3.connect('boeken.db')
    conn.row_factory = sqlite3.Row
    return conn

def row_to_dict(row):
    if row is None:
        return None
    return {
        "auteur": row["auteur"],
        "beschrijving": row["beschrijving"],
        "isbn": row["isbn"],
        "publicatiedatum": row["publicatiedatum"],
        "kaft_foto_url": row["kaft_foto_url"],
        "is_uitgeleend": bool(row["is_uitgeleend"]) if row["is_uitgeleend"] is not None else False,
        "uitgeleend_datum": row["uitgeleend_datum"],
        "uitgeleend_max_tot": row["uitgeleend_max_tot"]
    }

def get_all_boeken():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM boeken")
    rows = cursor.fetchall()
    conn.close()
    return [row_to_dict(row) for row in rows]

def get_boek_by_isbn(isbn):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM boeken WHERE isbn = ?", (isbn,))
    row = cursor.fetchone()
    conn.close()
    if row is None:
        raise BoekNotFoundException()
    return row_to_dict(row)

def create_boek(boek_data):
    required_fields = [
        "auteur",
        "beschrijving",
        "isbn",
        "publicatiedatum",
        "kaft_foto_url",
        "is_uitgeleend",
        "uitgeleend_datum",
        "uitgeleend_max_tot"
    ]
    for field in required_fields:
        if field not in boek_data:
            raise InvalidBoekDataException()
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO boeken (auteur, beschrijving, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                boek_data["auteur"],
                boek_data["beschrijving"],
                boek_data["isbn"],
                boek_data["publicatiedatum"],
                boek_data["kaft_foto_url"],
                int(boek_data["is_uitgeleend"]),
                boek_data["uitgeleend_datum"],
                boek_data["uitgeleend_max_tot"]
            ),
        )
        conn.commit()
        conn.close()
        return boek_data
    except Exception:
        conn.close()
        raise InvalidBoekDataException()

def update_boek(isbn, boek_data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM boeken WHERE isbn = ?", (isbn,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise BoekNotFoundException()
    try:
        cursor.execute(
            """
            UPDATE boeken
            SET auteur = ?, beschrijving = ?, publicatiedatum = ?, kaft_foto_url = ?, is_uitgeleend = ?, uitgeleend_datum = ?, uitgeleend_max_tot = ?
            WHERE isbn = ?
            """,
            (
                boek_data["auteur"],
                boek_data["beschrijving"],
                boek_data["publicatiedatum"],
                boek_data["kaft_foto_url"],
                int(boek_data["is_uitgeleend"]),
                boek_data["uitgeleend_datum"],
                boek_data["uitgeleend_max_tot"],
                isbn,
            ),
        )
        conn.commit()
        conn.close()
        new_row = boek_data.copy()
        new_row["isbn"] = isbn
        return new_row
    except Exception:
        conn.close()
        raise InvalidBoekDataException()

def delete_boek(isbn):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM boeken WHERE isbn = ?", (isbn,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        raise BoekNotFoundException()
    cursor.execute("DELETE FROM boeken WHERE isbn = ?", (isbn,))
    conn.commit()
    conn.close()
    return True

def register_routes(app):
    @app.route("/boeken", methods=["GET"])
    def boeken_get_all():
        try:
            boeken = get_all_boeken()
            return jsonify(boeken), 200
        except Exception:
            return '', 400

    @app.route("/boeken/<isbn>", methods=["GET"])
    def boeken_get_by_isbn(isbn):
        try:
            boek = get_boek_by_isbn(isbn)
            return jsonify(boek), 200
        except BoekNotFoundException:
            return '', 404

    @app.route("/boeken", methods=["POST"])
    def boeken_create():
        data = request.get_json()
        try:
            boek = create_boek(data)
            return jsonify(boek), 201
        except InvalidBoekDataException:
            return '', 400

    @app.route("/boeken/<isbn>", methods=["PUT"])
    def boeken_update(isbn):
        data = request.get_json()
        try:
            boek = update_boek(isbn, data)
            return jsonify(boek), 200
        except BoekNotFoundException:
            return '', 404
        except InvalidBoekDataException:
            return '', 400

    @app.route("/boeken/<isbn>", methods=["DELETE"])
    def boeken_delete(isbn):
        try:
            delete_boek(isbn)
            return '', 204
        except BoekNotFoundException:
            return '', 404