import os
import sqlite3
import database_exceptions

DB_PATH = os.path.join(os.path.dirname(__file__), 'bibliotheek.db')

def get_connection():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        raise database_exceptions.DatabaseSetupError(str(e))

def init_db():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS boeken ("
            "auteur TEXT,"
            "beschrijving TEXT,"
            "isbn TEXT,"
            "publicatiedatum DATE,"
            "kaft_foto_url TEXT,"
            "is_uitgeleend BOOLEAN,"
            "uitgeleend_datum DATE,"
            "uitgeleend_max_tot DATE)"
        )
        conn.commit()
    except Exception as e:
        raise database_exceptions.DatabaseSetupError(str(e))
    finally:
        if conn:
            conn.close()