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
            raise InvalidBoekDataException("Boek data is niet geldig")
        if self.repository.exists_by_isbn(data["isbn"]):
            raise BoekAlreadyExistsException(f"Boek met ISBN {data['isbn']} bestaat al.")
        # Neem alle potentiële sleutelwaarden op uit SCHEMA_FIELDS, evt. defaults
        boek_args = {}
        for key in SCHEMA_FIELDS:
            boek_args[key] = data.get(key)
        # Extra veld: jaar
        jaar = data.get("jaar")
        boek = self.repository.add(
            auteur=boek_args['auteur'],
            beschrijving=boek_args['beschrijving'],
            is_uitgeleend=boek_args.get('is_uitgeleend', 0),
            isbn=boek_args['isbn'],
            kaft_foto_url=boek_args['kaft_foto_url'],
            publicatiedatum=boek_args['publicatiedatum'],
            titel=boek_args['titel'],
            uitgeleend_datum=boek_args['uitgeleend_datum'],
            uitgeleend_max_tot=boek_args['uitgeleend_max_tot'],
            jaar=jaar,
        )
        return boek
