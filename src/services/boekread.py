from database import get_connection
from src.services.boekread_exceptions import BoekReadException, BoekReadNotFoundException

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, titel, auteur, jaar FROM Boek WHERE id = ?", (boek_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "titel": row[1],
                "auteur": row[2],
                "jaar": row[3]
            }
        else:
            return None

    def get_all(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, titel, auteur, jaar FROM Boek")
        rows = cursor.fetchall()
        boeken = []
        for row in rows:
            boeken.append({
                "id": row[0],
                "titel": row[1],
                "auteur": row[2],
                "jaar": row[3]
            })
        return boeken

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection
        self.repository = BoekRepository(self.db_connection)

    def get_boek_by_id(self, boek_id):
        try:
            boek = self.repository.get_by_id(boek_id)
            if not boek:
                raise BoekReadNotFoundException(f"Boek met id {boek_id} niet gevonden")
            return boek
        except BoekReadNotFoundException:
            raise
        except Exception as e:
            raise e

    def get_all_boeken(self):
        try:
            return self.repository.get_all()
        except Exception as e:
            raise e
