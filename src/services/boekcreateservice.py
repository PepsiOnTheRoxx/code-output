from src.services.boekcreateservice_exceptions import (
    BoekAlreadyExistsException,
    InvalidBoekDataException,
    BoekDatabaseException as BoekDatabaseException,
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
            raise InvalidBoekDataException("Ongeldige boekdata")
        if self.repository.exists_by_isbn(boek_data["isbn"]):
            raise BoekAlreadyExistsException("Boek al aanwezig")
        try:
            return self.repository.add(
                auteur=boek_data.get("auteur"),
                beschrijving=boek_data.get("beschrijving"),
                is_uitgeleend=boek_data.get("is_uitgeleend", 0),
                isbn=boek_data.get("isbn"),
                kaft_foto_url=boek_data.get("kaft_foto_url"),
                publicatiedatum=boek_data.get("publicatiedatum"),
                titel=boek_data.get("titel"),
                uitgeleend_datum=boek_data.get("uitgeleend_datum"),
                uitgeleend_max_tot=boek_data.get("uitgeleend_max_tot"),
                jaar=boek_data.get("jaar")
            )
        except Exception as exc:
            raise BoekDatabaseException(f"Database error: {exc}")
