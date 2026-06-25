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
                id=boek_id, titel=titel, auteur=auteur, isbn=isbn, beschrijving=beschrijving, is_uitgeleend=is_uitgeleend,
                kaft_foto_url=kaft_foto_url, publicatiedatum=publicatiedatum, uitgeleend_datum=uitgeleend_datum, uitgeleend_max_tot=uitgeleend_max_tot, jaar=jaar
            )
        except Exception as e:
            raise BoekCreateServiceDatabaseException(str(e))

class BoekCreateService:
    def __init__(self, db_connection=None, repository=None):
        if repository is not None:
            self.repo = repository
        else:
            self.db_connection = db_connection or get_connection()
            self.repo = BoekRepository(self.db_connection)

    def create_boek(self, boek_data):
        required = ['titel', 'auteur', 'isbn']
        if not all(k in boek_data and boek_data[k] for k in required):
            raise InvalidBoekDataException('titel, auteur, isbn zijn verplicht en mogen niet leeg zijn')
        if self.repo.exists_by_isbn(boek_data['isbn']):
            raise BoekAlreadyExistsException(f"Boek met ISBN {boek_data['isbn']} bestaat al.")
        return self.repo.add(
            auteur=boek_data['auteur'],
            beschrijving=boek_data.get('beschrijving'),
            is_uitgeleend=boek_data.get('is_uitgeleend', 0),
            isbn=boek_data['isbn'],
            kaft_foto_url=boek_data.get('kaft_foto_url'),
            publicatiedatum=boek_data.get('publicatiedatum'),
            titel=boek_data['titel'],
            uitgeleend_datum=boek_data.get('uitgeleend_datum'),
            uitgeleend_max_tot=boek_data.get('uitgeleend_max_tot'),
            jaar=boek_data.get('jaar'),
        )
