from src.services.boekread_exceptions import (
    BoekNotFoundException,
    BoekDatabaseConnectionException,
    BoekAttributeReadException,
    BoekInvalidQueryException,
)

class DatabaseException(Exception):
    '''Generic database error exception for BoekService.''' 
    pass

class Boek:
    def __init__(self, id, titel, auteur, jaar, genre):
        self.id = id
        self.titel = titel
        self.auteur = auteur
        self.jaar = jaar
        self.genre = genre

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_boek_by_id(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT id, titel, auteur, jaar, genre FROM boeken WHERE id = ?", (boek_id,)
            )
            row = cursor.fetchone()
            if not row:
                raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden")
            return Boek(*row)
        except BoekNotFoundException:
            raise
        except Exception as e:
            raise DatabaseException(f"Databasefout bij het ophalen van boek: {str(e)}")

    def get_all_boeken(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, titel, auteur, jaar, genre FROM boeken")
            rows = cursor.fetchall()
            return [Boek(*row) for row in rows]
        except Exception as e:
            raise DatabaseException(f"Databasefout bij het ophalen van boeken: {str(e)}")
