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
                titel=row[SCHEMA_FIELDS.index('titel')+1],
                auteur=row[SCHEMA_FIELDS.index('auteur')+1],
                isbn=row[SCHEMA_FIELDS.index('isbn')+1],
                beschrijving=row[SCHEMA_FIELDS.index('beschrijving')+1],
                is_uitgeleend=row[SCHEMA_FIELDS.index('is_uitgeleend')+1],
                kaft_foto_url=row[SCHEMA_FIELDS.index('kaft_foto_url')+1],
                publicatiedatum=row[SCHEMA_FIELDS.index('publicatiedatum')+1],
                uitgeleend_datum=row[SCHEMA_FIELDS.index('uitgeleend_datum')+1],
                uitgeleend_max_tot=row[SCHEMA_FIELDS.index('uitgeleend_max_tot')+1]
            )
        return None

    def update_boek(self, boek):
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"""
            UPDATE boeken SET
                titel = ?,
                auteur = ?,
                isbn = ?,
                beschrijving = ?,
                is_uitgeleend = ?,
                kaft_foto_url = ?,
                publicatiedatum = ?,
                uitgeleend_datum = ?,
                uitgeleend_max_tot = ?
            WHERE rowid = ?
            """,
            (
                boek.titel,
                boek.auteur,
                boek.isbn,
                boek.beschrijving,
                boek.is_uitgeleend,
                boek.kaft_foto_url,
                boek.publicatiedatum,
                boek.uitgeleend_datum,
                boek.uitgeleend_max_tot,
                boek.id
            )
        )
        self.db_connection.commit()

class BoekService:
    def __init__(self, repository):
        self.repository = repository

    def update_boek(self, boek_id, data):
        boek = self.repository.get_boek_by_id(boek_id)
        if not boek:
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden.")
        if not data.get("titel") or not isinstance(data["titel"], str) or not data["titel"].strip():
            raise OngeldigeBoekDataException("Titel ontbreekt of is ongeldig.")
        if not data.get("auteur") or not isinstance(data["auteur"], str) or not data["auteur"].strip():
            raise OngeldigeBoekDataException("Auteur ontbreekt of is ongeldig.")
        if not data.get("isbn") or not isinstance(data["isbn"], str) or not data["isbn"].strip():
            raise OngeldigeBoekDataException("ISBN ontbreekt of is ongeldig.")
        boek.titel = data["titel"]
        boek.auteur = data["auteur"]
        boek.isbn = data["isbn"]
        boek.beschrijving = data.get("beschrijving", boek.beschrijving)
        boek.is_uitgeleend = data.get("is_uitgeleend", boek.is_uitgeleend)
        boek.kaft_foto_url = data.get("kaft_foto_url", boek.kaft_foto_url)
        boek.publicatiedatum = data.get("publicatiedatum", boek.publicatiedatum)
        boek.uitgeleend_datum = data.get("uitgeleend_datum", boek.uitgeleend_datum)
        boek.uitgeleend_max_tot = data.get("uitgeleend_max_tot", boek.uitgeleend_max_tot)
        try:
            self.repository.update_boek(boek)
        except Exception as e:
            raise BoekUpdateMisluktException(str(e))
