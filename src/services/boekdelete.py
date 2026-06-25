from database import get_connection
from src.services.boekdelete_exceptions import BoekNietGevondenException, DatabaseException

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def verwijder_boek(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM Boek WHERE id = ?", (boek_id,))
            if cursor.rowcount == 0:
                raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden")
            self.db_connection.commit()
            return True
        except BoekNietGevondenException:
            raise
        except Exception as e:
            raise DatabaseException(str(e))

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            db_connection = get_connection()
        self.repo = BoekRepository(db_connection)

    def verwijder_boek(self, boek_id):
        return self.repo.verwijder_boek(boek_id)