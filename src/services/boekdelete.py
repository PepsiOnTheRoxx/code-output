from src.services.boekdelete_exceptions import BoekNietGevondenException, BoekDeleteException
from database import get_connection

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection

    def find_boek_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT rowid, * FROM boeken WHERE rowid = ?", (boek_id,))
            boek = cursor.fetchone()
            return boek
        except Exception as e:
            raise BoekDeleteException(str(e))

    def delete_boek(self, boek_id):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("DELETE FROM boeken WHERE rowid = ?", (boek_id,))
            if cursor.rowcount == 0:
                raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden")
            self.db_connection.commit()
        except Exception as e:
            self.db_connection.rollback()
            raise BoekDeleteException(str(e))

    def verwijder_boek(self, boek_id):
        boek = self.find_boek_by_id(boek_id)
        if boek is None:
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden")
        self.delete_boek(boek_id)
