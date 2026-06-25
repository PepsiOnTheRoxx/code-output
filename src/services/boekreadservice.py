import sqlite3
from src.services.boekreadservice_exceptions import BoekNotFoundException, DatabaseReadException

class BoekReadService:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_boek_by_id(self, boek_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, titel, auteur FROM boeken WHERE id = ?", (boek_id,))
            row = cursor.fetchone()
            conn.close()
            if row is None:
                raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden.")
            return {"id": row[0], "titel": row[1], "auteur": row[2]}
        except BoekNotFoundException:
            raise
        except Exception as e:
            raise DatabaseReadException(str(e))

    def get_all_boeken(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, titel, auteur FROM boeken")
            rows = cursor.fetchall()
            conn.close()
            return [{"id": row[0], "titel": row[1], "auteur": row[2]} for row in rows]
        except Exception as e:
            raise DatabaseReadException(str(e))
