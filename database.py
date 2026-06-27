import os
import sqlite3
from database_exceptions import DatabaseSetupException

DB_PATH = os.path.join(os.path.dirname(__file__), 'bibliotheek.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = None
    cursor = None
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
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

class DatabaseSetup:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH

    def initialize_database(self):
        conn = None
        cursor = None
        try:
            conn = sqlite3.connect(self.db_path)
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
            raise DatabaseSetupException(str(e))
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()