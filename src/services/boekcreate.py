from src.services.boekcreate_exceptions import BoekCreateDuplicateException, BoekCreateDatabaseException

class BoekCreateService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_boek(self, boek_data):
        cursor = self.db_connection.cursor()
        try:
            # Check of boek met deze ISBN al bestaat
            query_exists = "SELECT 1 FROM boeken WHERE isbn=?"
            cursor.execute(query_exists, (boek_data["isbn"],))
            if cursor.fetchone() is not None:
                raise BoekCreateDuplicateException()
            # Insert boekgegevens
            query_insert = (
                "INSERT INTO boeken (titel, auteur, isbn, publicatiejaar, genre, taal, uitgever, pagina_aantal) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            )
            cursor.execute(
                query_insert,
                (
                    boek_data["titel"],
                    boek_data["auteur"],
                    boek_data["isbn"],
                    boek_data["publicatiejaar"],
                    boek_data["genre"],
                    boek_data["taal"],
                    boek_data["uitgever"],
                    boek_data["pagina_aantal"],
                ),
            )
            if cursor.rowcount == 0:
                raise BoekCreateDatabaseException()
            self.db_connection.commit()
        except BoekCreateDuplicateException:
            raise
        except Exception:
            self.db_connection.rollback()
            raise BoekCreateDatabaseException()
