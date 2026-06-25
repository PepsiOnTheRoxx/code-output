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
            '''
        CREATE TABLE IF NOT EXISTS boeken (
            auteur TEXT,
            beschrijving TEXT,
            is_uitgeleend BOOLEAN,
            isbn TEXT,
            kaft_foto_url TEXT,
            publicatiedatum DATE,
            titel TEXT,
            uitgeleend_datum DATE,
            uitgeleend_max_tot DATE
        )
        '''
        )
        conn.commit()
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        raise DatabaseSetupException(str(e))
    finally:
        if conn:
            conn.close()

class DatabaseSetup:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def initialize_database(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                '''
        CREATE TABLE IF NOT EXISTS boeken (
            auteur TEXT,
            beschrijving TEXT,
            is_uitgeleend BOOLEAN,
            isbn TEXT,
            kaft_foto_url TEXT,
            publicatiedatum DATE,
            titel TEXT,
            uitgeleend_datum DATE,
            uitgeleend_max_tot DATE
        )
        '''
            )
            conn.commit()
        except sqlite3.DatabaseError as e:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
                conn.close()
            raise DatabaseSetupException(str(e))
        except Exception as e:
            if conn:
                try:
                    conn.rollback()
                except Exception:
                    pass
                conn.close()
            raise DatabaseSetupException(str(e))
        else:
            if conn:
                conn.close()
