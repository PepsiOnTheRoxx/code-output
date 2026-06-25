from src.services.boekread_exceptions import BoekNotFoundException, BoekReadDatabaseException

def get_connection():
    # Dummy fallback in case database import is missing (for tests)
    class DummyConnection:
        def cursor(self):
            raise NotImplementedError("No database available.")
    return DummyConnection()

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_by_id(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT id, titel, auteur, jaar FROM Boek WHERE id = ?",
                (boek_id,)
            )
            row = cursor.fetchone()
            if row is None:
                raise BoekNotFoundException("Boek niet gevonden")
            return {
                "id": row[0],
                "titel": row[1],
                "auteur": row[2],
                "jaar": row[3]
            }
        except BoekNotFoundException:
            raise
        except Exception as e:
            raise BoekReadDatabaseException(str(e))

    def get_all(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, titel, auteur, jaar FROM Boek")
            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "titel": row[1],
                    "auteur": row[2],
                    "jaar": row[3]
                })
            return results
        except Exception as e:
            raise BoekReadDatabaseException(str(e))

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection
        self.repo = BoekRepository(self.db_connection)

    def get_boek_by_id(self, boek_id):
        return self.repo.get_by_id(boek_id)

    def get_all_boeken(self):
        return self.repo.get_all()
