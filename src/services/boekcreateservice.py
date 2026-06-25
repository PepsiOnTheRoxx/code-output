from src.services.boekcreateservice_exceptions import (
    BoekAlreadyExistsException,
    InvalidBoekDataException,
    BoekDatabaseException,
    BoekServiceDependencyException,
)
from database import get_connection


class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def exists_by_isbn(self, isbn):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT 1 FROM Boek WHERE isbn = ?", (isbn,))
            return cursor.fetchone() is not None
        except Exception as e:
            raise BoekDatabaseException(str(e))

    def add(self, titel, auteur, isbn):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT INTO Boek (titel, auteur, isbn) VALUES (?, ?, ?)", (titel, auteur, isbn)
            )
            self.db_connection.commit()
            boek_id = cursor.lastrowid
            return type("Boek", (), {"id": boek_id, "titel": titel, "auteur": auteur, "isbn": isbn})()
        except Exception as e:
            raise BoekDatabaseException(str(e))


class BoekCreateService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection
        self.repository = BoekRepository(self.db_connection)

    def _validate_boek_data(self, data):
        required = ["titel", "auteur", "isbn"]
        if not isinstance(data, dict):
            return False
        for key in required:
            if key not in data or not isinstance(data[key], str) or not data[key].strip():
                return False
        return True

    def create_boek(self, boek_data):
        if not self._validate_boek_data(boek_data):
            raise InvalidBoekDataException("Missing or invalid boek data.")
        isbn = boek_data["isbn"]
        try:
            if self.repository.exists_by_isbn(isbn):
                raise BoekAlreadyExistsException("Boek already exists with isbn: {}".format(isbn))
            created_boek = self.repository.add(
                titel=boek_data["titel"].strip(),
                auteur=boek_data["auteur"].strip(),
                isbn=boek_data["isbn"].strip(),
            )
            return created_boek
        except BoekAlreadyExistsException:
            raise
        except BoekDatabaseException:
            raise
        except Exception as e:
            raise BoekServiceDependencyException(str(e))