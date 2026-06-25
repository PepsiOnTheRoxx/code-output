from src.services.boekcreate_exceptions import BoekCreateDuplicateException, BoekCreateDatabaseException

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_boek(
        self,
        isbn,
        titel,
        auteur,
        uitgever,
        uitgiftejaar,
        genre,
        taal,
        pagina_aantal,
        beschrijving
    ):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                "SELECT 1 FROM boeken WHERE isbn = ?", (isbn,)
            )
            if cursor.fetchone():
                raise BoekCreateDuplicateException("Boek met dit ISBN bestaat al.")
            cursor.execute(
                "INSERT INTO boeken (isbn, titel, auteur, uitgever, uitgiftejaar, genre, taal, pagina_aantal, beschrijving) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    isbn,
                    titel,
                    auteur,
                    uitgever,
                    uitgiftejaar,
                    genre,
                    taal,
                    pagina_aantal,
                    beschrijving
                )
            )
            self.db_connection.commit()
        except BoekCreateDuplicateException:
            raise
        except Exception as e:
            raise BoekCreateDatabaseException(str(e))
