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
        if cursor.rowcount == 0:
            raise BoekNietGevondenException("Boek niet gevonden voor update")
        self.db_connection.commit()

class BoekService:
    def __init__(self, repo):
        self.repo = repo

    def update_boek(self, boek_id, data):
        # Validatie: titel, auteur, isbn verplicht + string
        titel = data.get('titel')
        auteur = data.get('auteur')
        isbn = data.get('isbn')
        if not titel or not isinstance(titel, str):
            raise OngeldigeBoekDataException('Titel is verplicht en mag niet leeg zijn')
        if not auteur or not isinstance(auteur, str):
            raise OngeldigeBoekDataException('Auteur is verplicht en mag niet leeg zijn')
        if not isbn or not isinstance(isbn, str):
            raise OngeldigeBoekDataException('ISBN is verplicht en mag niet leeg zijn')
        oud_boek = self.repo.get_boek_by_id(boek_id)
        if oud_boek is None:
            raise BoekNietGevondenException(f'Boek met id {boek_id} niet gevonden')
        # Update bestaande Boek object velden op basis van data (fallback op oud_boek als field ontbreekt)
        boek = Boek(
            id=boek_id,
            titel=data.get('titel', oud_boek.titel),
            auteur=data.get('auteur', oud_boek.auteur),
            isbn=data.get('isbn', oud_boek.isbn),
            beschrijving=data.get('beschrijving', oud_boek.beschrijving),
            is_uitgeleend=data.get('is_uitgeleend', oud_boek.is_uitgeleend),
            kaft_foto_url=data.get('kaft_foto_url', oud_boek.kaft_foto_url),
            publicatiedatum=data.get('publicatiedatum', oud_boek.publicatiedatum),
            uitgeleend_datum=data.get('uitgeleend_datum', oud_boek.uitgeleend_datum),
            uitgeleend_max_tot=data.get('uitgeleend_max_tot', oud_boek.uitgeleend_max_tot)
        )
        try:
            self.repo.update_boek(boek)
            return boek
        except BoekNietGevondenException:
            raise
        except Exception as e:
            raise BoekUpdateMisluktException(str(e))
