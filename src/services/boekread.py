from database import get_connection
from src.services.boekread_exceptions import BoekNotFoundException, BoekReadInvalidInputException

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, titel, auteur FROM boek WHERE id = ?", (boek_id,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "titel": row[1], "auteur": row[2]}
        return None

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection
        self.repository = BoekRepository(self.db_connection)

    def read_boek(self, boek_id):
        if boek_id is None or not isinstance(boek_id, int) or boek_id <= 0:
            raise BoekReadInvalidInputException()
        boek = self.repository.get_by_id(boek_id)
        if boek is None:
            raise BoekNotFoundException()
        return boek