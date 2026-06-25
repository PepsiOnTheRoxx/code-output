from src.services.boekdelete_exceptions import BoekNietGevondenException, DatabaseFoutException

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def verwijder_boek(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('DELETE FROM boeken WHERE id = ?', (boek_id,))
            if cursor.rowcount == 0:
                raise BoekNietGevondenException()
            self.db_connection.commit()
            return True
        except BoekNietGevondenException:
            raise
        except Exception:
            raise DatabaseFoutException()