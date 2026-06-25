from database import get_connection
from src.services.boekcreate_exceptions import (
    BoekCreateDuplicateISBNException,
    BoekCreateInvalidDataException,
    BoekCreateDatabaseException,
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
            raise BoekCreateDatabaseException(str(e))

    def create(self, boek_data):
        # Zorg dat alle kolommen (fixed volgorde per schema) aanwezig zijn (ook als None)
        kolommen = [
            "auteur",
            "beschrijving",
            "is_uitgeleend",
            "isbn",
            "kaft_foto_url",
            "publicatiedatum",
            "titel",
            "uitgeleend_datum",
            "uitgeleend_max_tot",
        ]
        insert_values = [boek_data.get(k) for k in kolommen]
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
                insert_values,
            )
            self.db_connection.commit()
            return boek_data
        except Exception as e:
            self.db_connection.rollback()
            raise BoekCreateDatabaseException(str(e))

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
            raise BoekCreateInvalidDataException("titel is verplicht")
        if not isbn or not str(isbn).strip():
            raise BoekCreateInvalidDataException("isbn is verplicht")
        boek_data = {
            "auteur": auteur,
            "beschrijving": beschrijving,
            "is_uitgeleend": is_uitgeleend,
            "isbn": isbn,
            "kaft_foto_url": kaft_foto_url,
            "publicatiedatum": publicatiedatum,
            "titel": titel,
            "uitgeleend_datum": uitgeleend_datum,
            "uitgeleend_max_tot": uitgeleend_max_tot,
        }

        if self.repo.exists(isbn=isbn):
            raise BoekCreateDuplicateISBNException("Boek met dit ISBN bestaat al")
        try:
            # Zorg dat alle attributen als keys aanwezig zijn, None is toegestaan (zoals default in database)
            return self.repo.create(boek_data)
        except BoekCreateDatabaseException as e:
            raise BoekCreateDatabaseException(str(e))
