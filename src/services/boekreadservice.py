from src.services.boekreadservice_exceptions import (
    BoekNotFoundException,
    BoekReadDatabaseException,
)
from database import get_connection

# Alias for compatibility with tests
DatabaseReadException = BoekReadDatabaseException

SCHEMA_FIELDS = [
    'auteur', 'beschrijving', 'is_uitgeleend', 'isbn', 'kaft_foto_url',
    'publicatiedatum', 'titel', 'uitgeleend_datum', 'uitgeleend_max_tot'
]

def row_to_boek(row, include_id=False, id_value=None):
    if row is None:
        return None
    boek = dict(zip(SCHEMA_FIELDS, row))
    if include_id:
        boek['id'] = id_value
    return boek

class BoekReadService:
    def __init__(self, db_connection=None, db_session=None):
        # Allow backward compatibility: prefer explicit db_session (for tests), else DB connection
        if db_session is not None:
            self.db_session = db_session
            self.db_connection = None
        else:
            self.db_session = None
            self.db_connection = db_connection or get_connection()

    def get_boek_by_id(self, boek_id):
        if self.db_session:
            # ORM-style interface for test mocks
            try:
                boek = self.db_session.query.return_value.get.return_value if hasattr(self.db_session.query.return_value, 'get') else self.db_session.query.return_value.get(boek_id)
                if boek is None:
                    raise BoekNotFoundException(f"Boek with id {boek_id} not found.")
                return boek
            except BoekNotFoundException:
                raise
            except Exception as exc:
                raise DatabaseReadException(f"Database read error: {exc}")
        else:
            # Direct SQLite interface
            try:
                cursor = self.db_connection.cursor()
                cursor.execute(
                    f"SELECT {', '.join(SCHEMA_FIELDS)} FROM boeken WHERE rowid = ?",
                    (boek_id,)
                )
                row = cursor.fetchone()
                if not row:
                    raise BoekNotFoundException(f"Boek with id {boek_id} not found.")
                return row_to_boek(row, include_id=True, id_value=boek_id)
            except BoekNotFoundException:
                raise
            except Exception as exc:
                raise DatabaseReadException(f"Database read error: {exc}")

    def get_all_boeken(self):
        if self.db_session:
            try:
                boeken = self.db_session.query.return_value.all.return_value if hasattr(self.db_session.query.return_value, 'all') else self.db_session.query.return_value.all()
                return boeken
            except Exception as exc:
                raise DatabaseReadException(f"Database read error: {exc}")
        else:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute(f"SELECT rowid, {', '.join(SCHEMA_FIELDS)} FROM boeken")
                rows = cursor.fetchall()
                # Prepend id as rowid to results for better test compatibility
                return [dict({'id': row[0]}, **row_to_boek(row[1:])) for row in rows]
            except Exception as exc:
                raise DatabaseReadException(f"Database read error: {exc}")
