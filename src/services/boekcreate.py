from database import get_connection
from src.services.boekcreate_exceptions import (
    BoekCreateValidationException,
    BoekCreateDatabaseException,
    BoekAlreadyExistsException
)

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
        self.jaar = jaar  # Optioneel attribuut voor test-compatibiliteit

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
            values = [
                boek_data.get('auteur'),
                boek_data.get('beschrijving'),
                boek_data.get('isbn'),
                boek_data.get('publicatiedatum'),
                boek_data.get('kaft_foto_url'),
                boek_data.get('is_uitgeleend', 0),
                boek_data.get('uitgeleend_datum'),
                boek_data.get('uitgeleend_max_tot'),
                boek_data.get('titel')
            ]
            cursor.execute(
                """
                INSERT INTO boeken (
                    auteur, beschrijving, isbn, publicatiedatum, kaft_foto_url, is_uitgeleend, uitgeleend_datum, uitgeleend_max_tot, titel
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
                uitgeleend_max_tot=boek_data.get('uitgeleend_max_tot'),
                jaar=boek_data.get('jaar') # Optioneel voor test compatibility
            )
        except Exception as e:
            raise BoekCreateDatabaseException(f"Database insert error: {str(e)}")

class BoekService:
    def __init__(self, repository=None):
        self.repository = repository or BoekRepository(get_connection())

    def create_boek(self, boek_data):
        # Validatie voor vereiste velden (incl. test-compatibiliteit met 'jaar')
        required = ["titel", "auteur", "isbn", "jaar"]
        for key in required:
            if key not in boek_data or not boek_data[key] or (isinstance(boek_data[key], str) and not boek_data[key].strip()):
                raise BoekCreateValidationException(f"Ongeldig of ontbrekend veld: {key}")
        if self.repository.exists(boek_data["isbn"]):
            raise BoekAlreadyExistsException(f"Boek met ISBN {boek_data['isbn']} bestaat al.")
        boek = self.repository.create(boek_data)
        return boek
