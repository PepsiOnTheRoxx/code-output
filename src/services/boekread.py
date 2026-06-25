from database import get_connection
from src.services.boekread_exceptions import BoekNotFoundException

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_boek_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT id, titel, auteur, isbn FROM boek WHERE id = ?", (boek_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "titel": row[1],
                "auteur": row[2],
                "isbn": row[3]
            }
        return None

    def get_all_boeken(self):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "SELECT id, titel, auteur, isbn FROM boek"
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "titel": row[1],
                "auteur": row[2],
                "isbn": row[3]
            }
            for row in rows
        ]

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            db_connection = get_connection()
        self.db_connection = db_connection
        self.boek_repo = BoekRepository(self.db_connection)

    def lees_boek_by_id(self, boek_id):
        try:
            boek = self.boek_repo.get_boek_by_id(boek_id)
            if boek is None:
                raise BoekNotFoundException()
            return boek
        except Exception as exc:
            raise exc

    def lees_alle_boeken(self):
        try:
            return self.boek_repo.get_all_boeken()
        except Exception as exc:
            raise exc
