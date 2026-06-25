from database import get_connection
from src.services.boekread_exceptions import BoekNotFoundException, BoekReadException

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_all_boeken(self):
        cursor = self.db_connection.cursor()
        # Gebruik rowid als id
        cursor.execute("SELECT rowid, titel, auteur FROM boeken")
        rows = cursor.fetchall()
        result = [{"id": row[0], "titel": row[1], "auteur": row[2]} for row in rows]
        return result

    def get_boek_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT rowid, titel, auteur FROM boeken WHERE rowid = ?", (boek_id,))
        row = cursor.fetchone()
        if row is not None:
            return {"id": row[0], "titel": row[1], "auteur": row[2]}
        return None

class BoekService:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_connection()
        self.boek_repository = BoekRepository(self.db_connection)

    def get_all_boeken(self):
        try:
            return self.boek_repository.get_all_boeken()
        except Exception as e:
            raise BoekReadException() from e

    def get_boek_by_id(self, boek_id):
        try:
            result = self.boek_repository.get_boek_by_id(boek_id)
            if result is None:
                raise BoekNotFoundException()
            return result
        except BoekNotFoundException:
            raise
        except TypeError:
            # explicit: bubble up type error, don't wrap in BoekReadException
            raise
        except Exception as e:
            raise BoekReadException() from e
