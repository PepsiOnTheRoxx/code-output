from src.services.boekupdateservice_exceptions import (
    BoekNietGevondenException,
    OngeldigeBoekDataException,
    BoekUpdateMisluktException,
    BoekServiceDatabaseException,
)
from database import get_connection

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
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_connection()

    def get_boek_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"SELECT rowid, {', '.join(SCHEMA_FIELDS)} FROM boeken WHERE rowid = ?",
            (boek_id,)
        )
        row = cursor.fetchone()
        if row:
            return Boek(
                id=row[0],
                auteur=row[1],
                beschrijving=row[2],
                is_uitgeleend=row[3],
                isbn=row[4],
                kaft_foto_url=row[5],
                publicatiedatum=row[6],
                titel=row[7],
                uitgeleend_datum=row[8],
                uitgeleend_max_tot=row[9]
            )
        return None

    def update_boek(self, boek):
        if not boek.titel or not boek.auteur or not boek.isbn:
            raise OngeldigeBoekDataException("Titel, auteur en isbn zijn verplicht")
        cursor = self.db_connection.cursor()
        cursor.execute(
            f'''
            UPDATE boeken SET
                auteur = ?,
                beschrijving = ?,
                is_uitgeleend = ?,
                isbn = ?,
                kaft_foto_url = ?,
                publicatiedatum = ?,
                titel = ?,
                uitgeleend_datum = ?,
                uitgeleend_max_tot = ?
            WHERE rowid = ?
            ''',
            (
                boek.auteur,
                boek.beschrijving,
                boek.is_uitgeleend,
                boek.isbn,
                boek.kaft_foto_url,
                boek.publicatiedatum,
                boek.titel,
                boek.uitgeleend_datum,
                boek.uitgeleend_max_tot,
                boek.id
            )
        )
        if cursor.rowcount == 0:
            raise BoekNietGevondenException("Boek niet gevonden voor update")
        self.db_connection.commit()
        return boek

class BoekService:
    def __init__(self, boek_repository=None):
        self.repo = boek_repository or BoekRepository()

    def update_boek(self, boek_id, boek_data):
        bestaand_boek = self.repo.get_boek_by_id(boek_id)
        if bestaand_boek is None:
            raise BoekNietGevondenException("Boek niet gevonden")
        # Update attributes if present, else fallback to old value
        for field in SCHEMA_FIELDS + ['titel']:
            if field in boek_data and hasattr(bestaand_boek, field):
                setattr(bestaand_boek, field, boek_data[field])
        # Validatie: titel, auteur en isbn verplicht
        if not bestaand_boek.titel or not bestaand_boek.auteur or not bestaand_boek.isbn:
            raise OngeldigeBoekDataException('Titel, auteur en isbn zijn verplicht')
        return self.repo.update_boek(bestaand_boek)