from database import get_connection
from src.services.boekdelete_exceptions import (
    BoekNotFoundException,
    DeleteNotAllowedException,
    BoekVerwijderDatabaseException,
    BoekVerwijderConflictException,
    BoekNietGevondenException,
    BoekVerwijderPermissionDeniedException,
)
class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM Boek WHERE id = ?", (boek_id,))
        row = cursor.fetchone()
        if row:
            boek = type("Boek", (object,), {})()
            boek.id = row[0]
            return boek
        return None

    def delete(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM Boek WHERE id = ?", (boek_id,))
            if cursor.rowcount == 0:
                raise BoekNotFoundException("Boek met id {} niet gevonden".format(boek_id))
            self.db_connection.commit()
        except BoekNotFoundException:
            raise
        except DeleteNotAllowedException:
            raise
        except Exception as ex:
            raise BoekVerwijderDatabaseException("Error bij verwijderen boek: {}".format(ex)) from ex

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            db_connection = get_connection()
        self.db_connection = db_connection
        self._repository = BoekRepository(self.db_connection)

    def delete_boek(self, boek_id):
        boek = self._repository.get_by_id(boek_id)
        if not boek:
            raise BoekNotFoundException("Boek niet gevonden")
        self._repository.delete(boek_id)