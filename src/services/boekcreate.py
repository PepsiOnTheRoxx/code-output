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
            "titel": titel,
        }
        # Voeg alleen niet-None velden toe voor publicatiedatum / uitgeleend_datum / uitgeleend_max_tot
        if publicatiedatum is not None:
            boek_data["publicatiedatum"] = publicatiedatum
        if uitgeleend_datum is not None:
            boek_data["uitgeleend_datum"] = uitgeleend_datum
        if uitgeleend_max_tot is not None:
            boek_data["uitgeleend_max_tot"] = uitgeleend_max_tot

        if self.repo.exists(isbn=isbn):
            raise BoekCreateDuplicateISBNException("Boek met dit ISBN bestaat al")
        try:
            # ONLY pass niet-None values in boek_data
            filtered_data = {k: v for k, v in boek_data.items() if v is not None}
            return self.repo.create(filtered_data)
        except BoekCreateDatabaseException as e:
            raise BoekCreateDatabaseException(str(e))
