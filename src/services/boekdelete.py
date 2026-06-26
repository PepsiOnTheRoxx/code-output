from database import get_connection
from src.services.boekdelete_exceptions import (
    BoekNotFoundException,
    BoekDeleteException
)

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM boek WHERE id = ?", (boek_id,))
        row = cursor.fetchone()
        return row

    def delete(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM boek WHERE id = ?", (boek_id,))
        self.db_connection.commit()


class BoekService:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_connection()
        self._repo = BoekRepository(self.db_connection)

    def delete_boek(self, boek_id):
        if not isinstance(boek_id, int):
            raise TypeError("Boek ID must be an integer")
        boek = self._repo.get_by_id(boek_id)
        if not boek:
            raise BoekNotFoundException(f"Boek with id {boek_id} not found")
        try:
            self._repo.delete(boek_id)
        except Exception as e:
            raise BoekDeleteException(f"Failed to delete boek with id {boek_id}: {str(e)}")