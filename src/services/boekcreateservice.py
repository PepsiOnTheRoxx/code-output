from src.services.boekcreateservice_exceptions import (
    BoekAlreadyExistsException,
    InvalidBoekDataException,
    BoekCreateServiceDatabaseException,
)
from database import get_connection

SCHEMA_FIELDS = [
    'auteur', 'beschrijving', 'is_uitgeleend', 'isbn', 'kaft_foto_url',
    'publicatiedatum', 'titel', 'uitgeleend_datum', 'uitgeleend_max_tot'
]

class Boek:
    def __init__(self, id, titel, auteur, isbn, beschrijving=None, is_uitgeleend=0, kaft_foto_url=None, publicatiedatum=None, uitgeleend_datum=None, uitgeleend_max_tot=None, jaar=None):
        self.id = id
        self.titel = titel
        self.auteur = auteur
        self.isbn = isbn
        self.beschrijving = beschrijving
        self.is_uitgeleend = is_uitgeleend
        self.kaft_foto_url = kaft_foto_url
        self.publicatiedatum = publicatiedatum
        self.uitgeleend_datum = uitgeleend_datum
        self.uitgeleend_max_tot = uitgeleend_max_tot
        self.jaar = jaar

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
            return Boek(
                id=boek_id,
                titel=titel,
                auteur=auteur,
                isbn=isbn,
                beschrijving=beschrijving,
                is_uitgeleend=is_uitgeleend,
                kaft_foto_url=kaft_foto_url,
                publicatiedatum=publicatiedatum,
                uitgeleend_datum=uitgeleend_datum,
                uitgeleend_max_tot=uitgeleend_max_tot,
                jaar=jaar
            )
        except Exception as e:
            raise BoekCreateServiceDatabaseException(str(e))

class BoekCreateService:
    def __init__(self, db_connection=None, repository=None):
        if repository is not None:
            self.repo = repository
        else:
            self.repo = BoekRepository(db_connection or get_connection())

    def create_boek(self, boek_data):
        if (not boek_data.get("titel")
            or not boek_data.get("auteur")
            or not boek_data.get("isbn")):
            raise InvalidBoekDataException("titel, auteur en isbn verplicht")
        if self.repo.exists_by_isbn(boek_data["isbn"]):
            raise BoekAlreadyExistsException(f"Boek met ISBN {boek_data['isbn']} bestaat al")
        return self.repo.add(**{field: boek_data.get(field) for field in SCHEMA_FIELDS}, jaar=boek_data.get("jaar"))
