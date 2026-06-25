from src.services.boekcreate_exceptions import (
    BoekAlreadyExistsException,
    BoekMissingAttributeException,
    BoekInvalidAttributeException,
    BoekDatabaseException,
)

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_boek(self, boek_data):
        required_fields = [
            "titel",
            "auteur",
            "isbn",
            "jaartal",
            "categorie",
            "taal",
            "uitgever",
            "paginas",
            "prijs"
        ]
        for field in required_fields:
            if field not in boek_data:
                raise BoekMissingAttributeException(f">{field}< ontbreekt")
            if boek_data[field] is None:
                raise BoekInvalidAttributeException(f">{field}< is ongeldig")
        try:
            cursor = self.db_connection.cursor()
            select_sql = "SELECT 1 FROM boeken WHERE isbn = ?"
            cursor.execute(select_sql, (boek_data["isbn"],))
            if cursor.fetchone():
                raise BoekAlreadyExistsException("Boek met dit ISBN bestaat al.")

            insert_sql = (
                "INSERT INTO boeken (titel, auteur, isbn, jaartal, categorie, taal, uitgever, paginas, prijs) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            )
            cursor.execute(
                insert_sql,
                (
                    boek_data["titel"],
                    boek_data["auteur"],
                    boek_data["isbn"],
                    boek_data["jaartal"],
                    boek_data["categorie"],
                    boek_data["taal"],
                    boek_data["uitgever"],
                    boek_data["paginas"],
                    boek_data["prijs"],
                ),
            )
            self.db_connection.commit()
        except BoekAlreadyExistsException:
            raise
        except (BoekMissingAttributeException, BoekInvalidAttributeException):
            raise
        except Exception as ex:
            raise BoekDatabaseException(f"Database error: {ex}") from ex
