from src.services.boekdelete_exceptions import BoekNotFoundException, BoekDeleteDatabaseException

# Dummy fallback, in het echt zou dit van elders komen
class DummyConnection:
    def cursor(self):
        return DummyCursor()
    def commit(self):
        pass
class DummyCursor:
    def execute(self, *a, **kw):
        pass
    @property
    def rowcount(self):
        return 1

def get_connection():
    return DummyConnection()

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def verwijder_boek(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM boeken WHERE rowid = ?", (boek_id,))
            if cursor.rowcount == 0:
                raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden")
            self.db_connection.commit()
            return True
        except BoekNotFoundException:
            raise
        except Exception as e:
            raise BoekDeleteDatabaseException(str(e))

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            db_connection = get_connection()
        self.repo = BoekRepository(db_connection)

    def verwijder_boek(self, boek_id):
        return self.repo.verwijder_boek(boek_id)
