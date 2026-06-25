import os
import sqlite3
from database_exceptions import DatabaseSetupException

DB_PATH = os.path.join(os.path.dirname(__file__), 'bibliotheek.db')

# Definieer de oorspronkelijke CREATE TABLE-statement exact zoals in de tests
CREATE_TABEL_SQL = """CREATE TABLE IF NOT EXISTS boeken (
            auteur TEXT,
            beschrijving TEXT,
            isbn TEXT,
            publicatiedatum DATE,
            kaft_foto_url TEXT,
            is_uitgeleend BOOLEAN,
            uitgeleend_datum DATE,
            uitgeleend_max_tot DATE
        )"""

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(CREATE_TABEL_SQL)
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        raise DatabaseSetupException from e
    finally:
        if conn:
            conn.close()

class DatabaseSetup:
    def __init__(self, db_path=None):
        self.db_path = db_path or DB_PATH

    def initialiseer_database(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(CREATE_TABEL_SQL)
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise DatabaseSetupException from e
        finally:
            if conn:
                conn.close()