from src.services.boekreadservice_exceptions import (
    BoekNotFoundException,
    BoekReadDatabaseException,
)
import sqlite3
from database import get_connection

# Alias for compatibility with tests
DatabaseReadException = BoekReadDatabaseException

SCHEMA_FIELDS = [
    'auteur', 'beschrijving', 'is_uitgeleend', 'isbn', 'kaft_foto_url',
    'publicatiedatum', 'titel', 'uitgeleend_datum', 'uitgeleend_max_tot'
]

def row_to_boek(row):
    if row is None:
        return None
    return dict(zip(SCHEMA_FIELDS, row))

class BoekReadService:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_connection()

    def get_boek_by_id(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                f"SELECT {', '.join(SCHEMA_FIELDS)} FROM boeken WHERE rowid = ?",
                (boek_id,)
            )
            row = cursor.fetchone()
            if not row:
                raise BoekNotFoundException(f"Boek with id {boek_id} not found.")
            return row_to_boek(row)
        except BoekNotFoundException:
            raise
        except Exception as exc:
            raise DatabaseReadException(f"Database read error: {exc}")

    def get_all_boeken(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(f"SELECT {', '.join(SCHEMA_FIELDS)} FROM boeken")
            rows = cursor.fetchall()
            return [row_to_boek(row) for row in rows]
        except Exception as exc:
            raise DatabaseReadException(f"Database read error: {exc}")
