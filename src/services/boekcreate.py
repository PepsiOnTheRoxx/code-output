from src.services.boekcreate_exceptions import BoekCreateAlreadyExistsException, BoekCreateDatabaseException

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create(self, boek_data):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                "SELECT 1 FROM boek WHERE isbn = %s",
                (boek_data['isbn'],)
            )
            if cursor.fetchone() is not None:
                raise BoekCreateAlreadyExistsException()

            cursor.execute(
                "INSERT INTO boek (titel, auteur, isbn, publicatiejaar, uitgeverij, pagina_count, genre, taal, samenvatting)"
                " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    boek_data['titel'],
                    boek_data['auteur'],
                    boek_data['isbn'],
                    boek_data['publicatiejaar'],
                    boek_data['uitgeverij'],
                    boek_data['pagina_count'],
                    boek_data['genre'],
                    boek_data['taal'],
                    boek_data['samenvatting'],
                )
            )
            if cursor.rowcount == 0:
                raise BoekCreateDatabaseException()
            self.db_connection.commit()
            return True
        except BoekCreateAlreadyExistsException:
            raise
        except Exception as e:
            try:
                self.db_connection.rollback()
            except Exception:
                pass
            raise BoekCreateDatabaseException() from e
