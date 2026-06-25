from database import get_connection
from src.services.boekupdate_exceptions import (
    BoekNotFoundException,
    InvalidBoekDataException,
    BoekUpdateDatabaseException
)

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_boek_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, titel, auteur, jaar, isbn FROM Boek WHERE id = ?", (boek_id,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "titel": row[1],
                "auteur": row[2],
                "jaar": row[3],
                "isbn": row[4]
            }
        return None

    def update_boek(self, boek_id, data):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute(
                "UPDATE Boek SET titel = ?, auteur = ?, jaar = ?, isbn = ? WHERE id = ?",
                (data["titel"], data["auteur"], data["jaar"], data["isbn"], boek_id)
            )
            updated = cursor.rowcount > 0
            self.db_connection.commit()
            return updated
        except Exception as e:
            self.db_connection.rollback()
            raise BoekUpdateDatabaseException(str(e))

def _is_valid_isbn(isbn):
    return isinstance(isbn, str) and len(isbn) == 13 and isbn.isdigit()

def _validate_boek_data(data):
    if not isinstance(data, dict):
        return False
    if not data.get("titel") or not isinstance(data["titel"], str) or len(data["titel"].strip()) == 0:
        return False
    if not data.get("auteur") or not isinstance(data["auteur"], str):
        return False
    if not isinstance(data.get("jaar"), int):
        return False
    if not _is_valid_isbn(data.get("isbn", "")):
        return False
    return True

class BoekService:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_connection()
        self.repo = BoekRepository(self.db_connection)

    def update_boek(self, boek_id, boek_data):
        if not _validate_boek_data(boek_data):
            raise InvalidBoekDataException("Ongeldige boekgegevens.")

        boek = self.repo.get_boek_by_id(boek_id)
        if not boek:
            raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden.")

        try:
            updated = self.repo.update_boek(boek_id, boek_data)
        except BoekUpdateDatabaseException as exc:
            raise
        except Exception as exc:
            raise

        return updated