from src.services.boekdeleteservice_exceptions import BoekNotFoundException, DatabaseDeleteException

class BoekDeleteService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def verwijder_boek(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM boeken WHERE id=?", (boek_id,))
            if cursor.rowcount == 0:
                raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden")
            self.db_connection.commit()
            return True
        except BoekNotFoundException:
            raise
        except Exception as e:
            raise DatabaseDeleteException(str(e))