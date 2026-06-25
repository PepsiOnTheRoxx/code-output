from database import get_connection
from src.services.boekcreate_exceptions import (
    BoekAlreadyExistsException,
    BoekCreateValidationException,
    BoekCreateDatabaseException,
)

class Boek:
    def __init__(self, id, titel, auteur, isbn, jaar):
        self.id = id
        self.titel = titel
        self.auteur = auteur
        self.isbn = isbn
        self.jaar = jaar

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def exists(self, isbn):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT 1 FROM boeken WHERE isbn = ?", (isbn,))
            return cursor.fetchone() is not None
        except Exception as e:
            raise BoekCreateDatabaseException(f"Database check error: {str(e)}")

    def create(self, boek_data):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT INTO boeken (titel, auteur, isbn, jaar) VALUES (?, ?, ?, ?)",
                (boek_data["titel"], boek_data["auteur"], boek_data["isbn"], boek_data["jaar"])
            )
            boek_id = cursor.lastrowid
            self.db_connection.commit()
            return Boek(
                id=boek_id,
                titel=boek_data["titel"],
                auteur=boek_data["auteur"],
                isbn=boek_data["isbn"],
                jaar=boek_data["jaar"],
            )
        except Exception as e:
            self.db_connection.rollback()
            raise BoekCreateDatabaseException(f"Database create error: {str(e)}")

class BoekService:
    def __init__(self, db_connection=None, repository=None):
        if repository is not None:
            self.repository = repository
            return
        if db_connection is None:
            db_connection = get_connection()
        self.repository = BoekRepository(db_connection)

    def create_boek(self, boek_data):
        self._validate_data(boek_data)
        if self.repository.exists(boek_data["isbn"]):
            raise BoekAlreadyExistsException("Boek bestaat al (duplicate ISBN)")
        return self.repository.create(boek_data)

    def _validate_data(self, boek_data):
        if not boek_data.get("titel") or not boek_data.get("titel").strip():
            raise BoekCreateValidationException("Titel mag niet leeg zijn")
        if not boek_data.get("auteur") or not boek_data.get("auteur").strip():
            raise BoekCreateValidationException("Auteur mag niet leeg zijn")
        if not boek_data.get("isbn") or not boek_data.get("isbn").strip():
            raise BoekCreateValidationException("ISBN mag niet leeg zijn")
        if boek_data.get("jaar") is None:
            raise BoekCreateValidationException("Jaar mag niet leeg zijn")