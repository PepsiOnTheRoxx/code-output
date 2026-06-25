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
    def __init__(self, repository=None):
        self.repository = repository or BoekRepository()

    def update_boek(self, boek_id, nieuwe_data):
        oud_boek = self.repository.get_boek_by_id(boek_id)
        if not oud_boek:
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden.")
        if not self._validate_boek_data(nieuwe_data):
            raise OngeldigeBoekDataException("Ongeldige boekdata.")

        # Update velden
        for key in SCHEMA_FIELDS:
            if key in nieuwe_data:
                setattr(oud_boek, key, nieuwe_data[key])
        try:
            self.repository.update_boek(oud_boek)
        except Exception as e:
            raise BoekUpdateMisluktException(str(e))

    def _validate_boek_data(self, data):
        required = ["titel", "auteur", "isbn"]
        if not isinstance(data, dict):
            return False
        for key in required:
            if key not in data or not isinstance(data[key], str) or not data[key].strip():
                return False
        return True
