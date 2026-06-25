from src.services.boekupdate_exceptions import BoekUpdateException, BoekNietGevondenException

class BoekUpdateService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def update_boek(self, boek_id, boek_data):
        try:
            cursor = self.db_connection.cursor()
            sql = "UPDATE boeken SET titel=?, auteur=?, isbn=? WHERE id=?"
            params = (boek_data['titel'], boek_data['auteur'], boek_data['isbn'], boek_id)
            cursor.execute(sql, params)
            if cursor.rowcount == 0:
                self.db_connection.rollback()
                raise BoekNietGevondenException()
            self.db_connection.commit()
        except BoekNietGevondenException:
            raise
        except Exception:
            self.db_connection.rollback()
            raise BoekUpdateException()
