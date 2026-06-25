import os
import sqlite3
from database_exceptions import (
    DatabaseSetupException,
    DatabaseSetupError,  # <-- fix: correctly import this name!
    DatabaseConnectionError,
    DatabaseTableCreationError,
    BoekAttribuutFout,
    BoekAuteurMissingError,
    BoekBeschrijvingMissingError,
    BoekIsbnMissingError,
    BoekTitelMissingError,
    BoekKaftFotoUrlError,
    BoekPublicatiedatumError,
    BoekIsUitgeleendTypeError,
    BoekUitgeleendDatumError,
    BoekUitgeleendMaxTotError,
)

DB_PATH = os.path.join(os.path.dirname(__file__), 'bibliotheek.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            """
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
            """
        )
        conn.commit()
    finally:
        if conn:
            conn.close()

class DatabaseSetup:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path

    def create_database_and_table(self):
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute(
                """
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
                """
            )
            conn.commit()
        except sqlite3.OperationalError as e:
            if conn:
                conn.close()
            raise DatabaseSetupError(str(e))
        except sqlite3.DatabaseError as e:
            if conn:
                conn.close()
            raise DatabaseSetupError(str(e))
        except Exception as e:
            if conn:
                conn.close()
            raise DatabaseSetupError(str(e))
        finally:
            # Only close if not close already
            try:
                if conn:
                    conn.close()
            except:
                pass
