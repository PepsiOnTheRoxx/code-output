from database import get_connection
from src.services.boekdelete_exceptions import (
    BoekNietGevondenException,
    BoekDeleteException,
    BoekDeleteMisluktException,
    OngeldigeBoekIdException,
)

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection

    def verwijder_boek(self, boek_id):
        boek = self.haal_boek_op(boek_id)
        if not boek:
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden")
        try:
            return self.verwijder_boek_db(boek_id)
        except (BoekDeleteException, BoekDeleteMisluktException, OngeldigeBoekIdException):
            raise
        except Exception as ex:
            raise ex

    def haal_boek_op(self, boek_id):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("SELECT id, titel FROM Boek WHERE id = ?", (boek_id,))
                row = cursor.fetchone()
                if row:
                    return {"id": row[0], "titel": row[1]}
                return None
        except Exception as ex:
            raise BoekDeleteException(f"Fout bij ophalen boek: {ex}")

    def verwijder_boek_db(self, boek_id):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("DELETE FROM Boek WHERE id = ?", (boek_id,))
                if cursor.rowcount == 0:
                    raise BoekDeleteMisluktException(f"Boek met id {boek_id} kon niet verwijderd worden")
            self.db_connection.commit()
            return True
        except (BoekDeleteMisluktException, OngeldigeBoekIdException):
            raise
        except Exception as ex:
            raise BoekDeleteException(f"Fout bij verwijderen boek: {ex}")