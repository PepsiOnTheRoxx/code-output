from database import get_connection
from src.services.boekread_exceptions import BoekNotFoundException

SCHEMA_FIELDS = [
    'auteur', 'beschrijving', 'is_uitgeleend', 'isbn', 'kaft_foto_url',
    'publicatiedatum', 'titel', 'uitgeleend_datum', 'uitgeleend_max_tot'
]

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_boek_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT rowid, {', '.join(SCHEMA_FIELDS)} FROM boeken WHERE rowid = ?",
            (boek_id,)
        )
        row = cursor.fetchone()
        if row:
            return dict(
                id=row[0],
                **{field: row[i+1] for i, field in enumerate(SCHEMA_FIELDS)}
            )
        return None

    def get_all_boeken(self):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT rowid, {', '.join(SCHEMA_FIELDS)} FROM boeken"
        )
        rows = cursor.fetchall()
        boeken = []
        for row in rows:
            boek = dict(
                id=row[0],
                **{field: row[i+1] for i, field in enumerate(SCHEMA_FIELDS)}
            )
            boeken.append(boek)
        return boeken

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            db_connection = get_connection()
        self.db_connection = db_connection
        self.boek_repo = BoekRepository(self.db_connection)

    def lees_boek_by_id(self, boek_id):
        try:
            boek = self.boek_repo.get_boek_by_id(boek_id)
            if boek is None:
                raise BoekNotFoundException()
            return boek
        except Exception as exc:
            raise exc

    def lees_alle_boeken(self):
        try:
            return self.boek_repo.get_all_boeken()
        except Exception as exc:
            raise exc
