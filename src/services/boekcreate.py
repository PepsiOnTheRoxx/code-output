from database import get_connection
from src.services.boekcreate_exceptions import (
    BoekCreateValidationException,
    BoekCreateDatabaseException,
)

# Define the exception expected by the tests
class BoekAlreadyExistsException(Exception):
    pass

# Gebruik alleen de kolommen die in het schema staan.
SCHEMA_FIELDS = [
    'auteur', 'beschrijving', 'is_uitgeleend', 'isbn', 'kaft_foto_url',
    'publicatiedatum', 'titel', 'uitgeleend_datum', 'uitgeleend_max_tot'
]

class Boek:
    def __init__(self, id, titel, auteur, isbn, beschrijving=None, is_uitgeleend=0, kaft_foto_url=None, publicatiedatum=None, uitgeleend_datum=None, uitgeleend_max_tot=None):
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

class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def exists(self, isbn):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT 1 FROM boeken WHERE isbn = ?", (isbn,))
            return cursor.fetchone() is not None
        except Exception as e:
            raise BoekCreateDatabaseException(f"Database check error: {str(e)}")

    def create(self, boek_data):
        try:
            cursor = self.db_connection.cursor()
            # vul standaardwaarden aan indien niet aanwezig (voor nullables)
            values = [
                boek_data.get('auteur'),
                boek_data.get('beschrijving'),
                boek_data.get('is_uitgeleend', 0),
                boek_data.get('isbn'),
                boek_data.get('kaft_foto_url'),
                boek_data.get('publicatiedatum'),
                boek_data.get('titel'),
                boek_data.get('uitgeleend_datum'),
                boek_data.get('uitgeleend_max_tot')
            ]
            cursor.execute(
                """
                INSERT INTO boeken (
                    auteur, beschrijving, is_uitgeleend, isbn, kaft_foto_url, publicatiedatum, titel, uitgeleend_datum, uitgeleend_max_tot
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                tuple(values)
            )
            boek_id = cursor.lastrowid
            self.db_connection.commit()
            return Boek(
                id=boek_id,
                titel=boek_data.get('titel'),
                auteur=boek_data.get('auteur'),
                isbn=boek_data.get('isbn'),
                beschrijving=boek_data.get('beschrijving'),
                is_uitgeleend=boek_data.get('is_uitgeleend', 0),
                kaft_foto_url=boek_data.get('kaft_foto_url'),
                publicatiedatum=boek_data.get('publicatiedatum'),
                uitgeleend_datum=boek_data.get('uitgeleend_datum'),
                uitgeleend_max_tot=boek_data.get('uitgeleend_max_tot')
            )
        except Exception as e:
            self.db_connection.rollback()
            raise BoekCreateDatabaseException(f"Database create error: {str(e)}")

class BoekService:
    def __init__(self, db_connection=None, repository=None):
        if repository is not None:
            self.repository = repository
            return
        if db_connection is None:
            db_connection = get_connection()
        self.repository = BoekRepository(db_connection)

    def create_boek(self, boek_data):
        self._validate_data(boek_data)
        if self.repository.exists(boek_data["isbn"]):
            raise BoekAlreadyExistsException("Boek bestaat al (duplicate ISBN)")
        return self.repository.create(boek_data)

    def _validate_data(self, boek_data):
        if not boek_data.get("titel") or not boek_data.get("titel").strip():
            raise BoekCreateValidationException("Titel mag niet leeg zijn")
        if not boek_data.get("auteur") or not boek_data.get("auteur").strip():
            raise BoekCreateValidationException("Auteur mag niet leeg zijn")
        if not boek_data.get("isbn") or not boek_data.get("isbn").strip():
            raise BoekCreateValidationException("ISBN mag niet leeg zijn")
        # 'jaar' verwijderen, want niet meer nodig
        # andere velden zijn optioneel volgens het schema
