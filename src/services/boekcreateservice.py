from src.services.boekcreateservice_exceptions import (
    BoekAlreadyExistsException,
    InvalidBoekDataException,
    BoekCreateServiceDatabaseException,
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
            raise BoekCreateServiceDatabaseException(str(e))

    def add(self, auteur, beschrijving=None, is_uitgeleend=0, isbn=None, kaft_foto_url=None, publicatiedatum=None, titel=None, uitgeleend_datum=None, uitgeleend_max_tot=None, jaar=None):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                """
                INSERT INTO boeken (
                    auteur, beschrijving, is_uitgeleend, isbn, kaft_foto_url, publicatiedatum, titel, uitgeleend_datum, uitgeleend_max_tot
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    auteur, beschrijving, is_uitgeleend, isbn, kaft_foto_url, publicatiedatum, titel, uitgeleend_datum, uitgeleend_max_tot
                )
            )
            self.db_connection.commit()
            boek_id = cursor.lastrowid
            # Maak een object/dict met ALLE velden van het schema terug, plus optioneel 'jaar'
            attrs = {
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
            }
            if jaar is not None:
                attrs["jaar"] = jaar
            return type("Boek", (), attrs)()
        except Exception as e:
            raise BoekCreateServiceDatabaseException(str(e))

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

    def create_boek(self, data):
        if not self._validate_boek_data(data):
            raise InvalidBoekDataException("Ongeldige boek data")
        isbn = data.get("isbn")
        if self.repository.exists_by_isbn(isbn):
            raise BoekAlreadyExistsException(f"Boek met ISBN {isbn} bestaat al")
        try:
            boek = self.repository.add(
                auteur=data.get("auteur"),
                beschrijving=data.get("beschrijving"),
                is_uitgeleend=data.get("is_uitgeleend", 0),
                isbn=data.get("isbn"),
                kaft_foto_url=data.get("kaft_foto_url"),
                publicatiedatum=data.get("publicatiedatum"),
                titel=data.get("titel"),
                uitgeleend_datum=data.get("uitgeleend_datum"),
                uitgeleend_max_tot=data.get("uitgeleend_max_tot"),
                jaar=data.get("jaar")
            )
            return boek
        except BoekCreateServiceDatabaseException as e:
            raise e
        except Exception as e:
            raise BoekServiceDependencyException(str(e))
