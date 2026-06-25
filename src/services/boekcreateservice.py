from src.services.boekcreateservice_exceptions import (
    BoekAlreadyExistsException,
    InvalidBoekDataException,
    BoekCreateServiceDatabaseException,
)
from database import get_connection

SCHEMA_FIELDS = [
    'auteur', 'beschrijving', 'isbn', 'publicatiedatum', 'kaft_foto_url',
    'is_uitgeleend', 'uitgeleend_datum', 'uitgeleend_max_tot', 'titel'
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
                    auteur, beschrijving, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot, titel
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    auteur, beschrijving, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot, titel
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

    def create_boek(self, data):
        # Validaties:
        if not data.get('titel') or not isinstance(data['titel'], str) or not data['titel'].strip():
            raise InvalidBoekDataException("Titel is verplicht en mag niet leeg zijn")
        if not data.get('auteur') or not isinstance(data['auteur'], str) or not data['auteur'].strip():
            raise InvalidBoekDataException("Auteur is verplicht en mag niet leeg zijn")
        if not data.get('isbn') or not isinstance(data['isbn'], str) or not data['isbn'].strip():
            raise InvalidBoekDataException("ISBN is verplicht en mag niet leeg zijn")
        # Controleer op duplicaat isbn
        if self.repo.exists_by_isbn(data['isbn']):
            raise BoekAlreadyExistsException("Boek met dit ISBN bestaat al")
        # Voeg toe
        return self.repo.add(
            auteur=data.get('auteur'),
            beschrijving=data.get('beschrijving'),
            is_uitgeleend=data.get('is_uitgeleend', 0),
            isbn=data.get('isbn'),
            kaft_foto_url=data.get('kaft_foto_url'),
            publicatiedatum=data.get('publicatiedatum'),
            titel=data.get('titel'),
            uitgeleend_datum=data.get('uitgeleend_datum'),
            uitgeleend_max_tot=data.get('uitgeleend_max_tot'),
            jaar=data.get('jaar')
        )
