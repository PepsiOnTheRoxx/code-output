from src.services.boekread_exceptions import (
    BoekNotFoundException,
    BoekDatabaseFoutException,
    BoekOphalenOnbekendeFoutException,
)

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_boek_by_id(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT id, titel, auteur FROM boeken WHERE id = ?", (boek_id,)
            )
            result = cursor.fetchone()
            if result is None:
                raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden")
            return result
        except BoekNotFoundException:
            raise
        except Exception as e:
            raise BoekDatabaseFoutException(f"Databasefout bij ophalen: {e}")

    def get_all_boeken(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, titel, auteur FROM boeken")
            result = cursor.fetchall()
            return result
        except Exception as e:
            raise BoekOphalenOnbekendeFoutException(f"Onbekende fout: {e}")