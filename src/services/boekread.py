import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from database import get_connection
from .boekread_exceptions import BoekNotFoundException, InvalidBoekIdException

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_by_id(self, boek_rowid):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT rowid, titel, auteur FROM boeken WHERE rowid = ?", (boek_rowid,))
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
            raise InvalidBoekIdException()
        boek = self.repository.get_by_id(boek_id)
        if boek is None:
            raise BoekNotFoundException()
        return boek
