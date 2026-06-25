from src.services.boekcreateservice_exceptions import (
    BoekAlreadyExistsException,
    InvalidBoekDataException,
    BoekDatabaseException,
    BoekServiceDependencyException,
)
from database import get_connection

SCHEMA_FIELDS = [
    'auteur', 'beschrijving', 'is_uitgeleend', 'isbn', 'kaft_foto_url',
    'publicatiedatum', 'titel', 'uitgeleend_datum', 'uitgeleend_max_tot'
]

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def exists_by_isbn(self, isbn):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT 1 FROM boeken WHERE isbn = ?", (isbn,))
            return cursor.fetchone() is not None
        except Exception as e:
            raise BoekDatabaseException(str(e))

    def add(self, titel, auteur, isbn, beschrijving=None, is_uitgeleend=0, kaft_foto_url=None, publicatiedatum=None, uitgeleend_datum=None, uitgeleend_max_tot=None):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """
                INSERT INTO boeken (
                    titel, auteur, isbn, beschrijving, is_uitgeleend, kaft_foto_url, publicatiedatum, uitgeleend_datum, uitgeleend_max_tot
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    titel, auteur, isbn, beschrijving, is_uitgeleend, kaft_foto_url, publicatiedatum, uitgeleend_datum, uitgeleend_max_tot
                )
            )
            self.db_connection.commit()
            boek_id = cursor.lastrowid
            # Maak een object/dict met ALLE velden van het schema terug
            return type("Boek", (), {
                "id": boek_id,
                "titel": titel,
                "auteur": auteur,
                "isbn": isbn,
                "beschrijving": beschrijving,
                "is_uitgeleend": is_uitgeleend,
                "kaft_foto_url": kaft_foto_url,
                "publicatiedatum": publicatiedatum,
                "uitgeleend_datum": uitgeleend_datum,
                "uitgeleend_max_tot": uitgeleend_max_tot
            })()
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
            # Vul alle schema-velden op, met defaults als ze niet geleverd zijn
            created_boek = self.repository.add(
                titel=boek_data["titel"].strip(),
                auteur=boek_data["auteur"].strip(),
                isbn=boek_data["isbn"].strip(),
                beschrijving=boek_data.get("beschrijving"),
                is_uitgeleend=boek_data.get("is_uitgeleend", 0),  # False als default
                kaft_foto_url=boek_data.get("kaft_foto_url"),
                publicatiedatum=boek_data.get("publicatiedatum"),
                uitgeleend_datum=boek_data.get("uitgeleend_datum"),
                uitgeleend_max_tot=boek_data.get("uitgeleend_max_tot")
            )
            return created_boek
        except BoekAlreadyExistsException:
            raise
        except BoekDatabaseException:
            raise
        except Exception as e:
            raise BoekServiceDependencyException(str(e))
