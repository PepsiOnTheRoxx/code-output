from src.services.boekdelete_exceptions import (
    BoekDeleteException,
    BoekNietGevondenException,
)

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def delete_boek(self, boek_id):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM boek WHERE id = ?", (boek_id,)
                )
                if cursor.rowcount == 0:
                    raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden.")
                self.db_connection.commit()
        except BoekNietGevondenException:
            raise
        except Exception as e:
            raise BoekDeleteException(f"Fout bij verwijderen van boek: {e}")