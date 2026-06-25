from database import get_connection
from src.services.boekcreate_exceptions import (
    BoekAlreadyExistsException,
    InvalidBoekDataException,
    DatabaseException,
)

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def exists(self, isbn):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT 1 FROM boeken WHERE isbn = ?", (isbn,))
            return cursor.fetchone() is not None
        except Exception as e:
            raise DatabaseException(str(e))

    def create(self, boek_data):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """
                INSERT INTO boeken (
                    auteur,
                    beschrijving,
                    is_uitgeleend,
                    isbn,
                    kaft_foto_url,
                    publicatiedatum,
                    titel,
                    uitgeleend_datum,
                    uitgeleend_max_tot
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    boek_data.get("auteur"),
                    boek_data.get("beschrijving"),
                    boek_data.get("is_uitgeleend"),
                    boek_data.get("isbn"),
                    boek_data.get("kaft_foto_url"),
                    boek_data.get("publicatiedatum"),
                    boek_data.get("titel"),
                    boek_data.get("uitgeleend_datum"),
                    boek_data.get("uitgeleend_max_tot"),
                ),
            )
            self.db_connection.commit()
            return boek_data
        except Exception as e:
            self.db_connection.rollback()
            raise DatabaseException(str(e))

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection
        self.repo = BoekRepository(self.db_connection)

    def create_boek(
        self,
        auteur=None,
        beschrijving=None,
        is_uitgeleend=None,
        isbn=None,
        kaft_foto_url=None,
        publicatiedatum=None,
        titel=None,
        uitgeleend_datum=None,
        uitgeleend_max_tot=None
    ):
        if titel is None or not str(titel).strip():
            raise InvalidBoekDataException("titel is verplicht")
        if not isbn or not str(isbn).strip():
            raise InvalidBoekDataException("isbn is verplicht")
        boek_data = {
            "auteur": auteur,
            "beschrijving": beschrijving,
            "is_uitgeleend": is_uitgeleend,
            "isbn": isbn,
            "kaft_foto_url": kaft_foto_url,
            "publicatiedatum": publicatiedatum,
            "titel": titel,
            "uitgeleend_datum": uitgeleend_datum if "uitgeleend_datum" in locals() or uitgeleend_datum is not None else None,
            "uitgeleend_max_tot": uitgeleend_max_tot if "uitgeleend_max_tot" in locals() or uitgeleend_max_tot is not None else None
        }
        if self.repo.exists(isbn=isbn):
            raise BoekAlreadyExistsException("Boek met dit ISBN bestaat al")
        try:
            return self.repo.create(boek_data)
        except DatabaseException as e:
            raise DatabaseException(str(e))