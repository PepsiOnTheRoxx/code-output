import os
import sqlite3
from database_exceptions import DatabaseSetupException

DB_PATH = os.path.join(os.path.dirname(__file__), 'bibliotheek.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS boeken ("
            "auteur TEXT, "
            "beschrijving TEXT, "
            "is_uitgeleend BOOLEAN, "
            "isbn TEXT, "
            "kaft_foto_url TEXT, "
            "publicatiedatum DATE, "
            "titel TEXT, "
            "uitgeleend_datum DATE, "
            "uitgeleend_max_tot DATE"
            ")"
        )
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseSetupException("Fout bij database setup: %s" % e)
    finally:
        if conn:
            conn.close()

class DatabaseSetup:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def setup(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS boeken ("
                "auteur TEXT, "
                "beschrijving TEXT, "
                "is_uitgeleend BOOLEAN, "
                "isbn TEXT, "
                "kaft_foto_url TEXT, "
                "publicatiedatum DATE, "
                "titel TEXT, "
                "uitgeleend_datum DATE, "
                "uitgeleend_max_tot DATE"
                ")"
            )
            conn.commit()
        except sqlite3.Error as e:
            raise DatabaseSetupException("Fout bij database setup: %s" % e)
        finally:
            if conn:
                conn.close()