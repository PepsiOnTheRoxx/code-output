from src.services.boekdelete_exceptions import BoekDeleteException, BoekNotFoundException

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def delete_boek(self, boek_id):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute("DELETE FROM boeken WHERE id = %s", (boek_id,))
                if cursor.rowcount == 0:
                    raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden.")
            self.db_connection.commit()
            return True
        except BoekNotFoundException:
            raise
        except Exception as e:
            raise BoekDeleteException(str(e))