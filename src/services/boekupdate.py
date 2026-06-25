from src.services.boekupdate_exceptions import (
    BoekNietGevondenException,
    OngeldigeBoekDataException,
)
from database import get_connection

SCHEMA_FIELDS = [
    'auteur', 'beschrijving', 'is_uitgeleend', 'isbn', 'kaft_foto_url',
    'publicatiedatum', 'titel', 'uitgeleend_datum', 'uitgeleend_max_tot'
]

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
            boek = dict(
                id=row[0],
                **{field: row[i+1] for i, field in enumerate(SCHEMA_FIELDS)}
            )
            return boek
        return None

    def update_boek(self, bestaande_boek, update_data):
        # Bestaande boek is dict met velden volgens SCHEMA_FIELDS plus 'id'
        boek_id = bestaande_boek['id']
        nieuwe_data = {}
        for field in SCHEMA_FIELDS:
            nieuwe_data[field] = update_data.get(field, bestaande_boek.get(field))
        # Validatie: titel, auteur en isbn zijn verplicht
        if not nieuwe_data['titel'] or not isinstance(nieuwe_data['titel'], str):
            raise OngeldigeBoekDataException('Titel is verplicht en mag niet leeg zijn')
        if not nieuwe_data['auteur'] or not isinstance(nieuwe_data['auteur'], str):
            raise OngeldigeBoekDataException('Auteur is verplicht en mag niet leeg zijn')
        if not nieuwe_data['isbn'] or not isinstance(nieuwe_data['isbn'], str):
            raise OngeldigeBoekDataException('ISBN is verplicht en mag niet leeg zijn')
        cursor = self.db_connection.cursor()
        cursor.execute(
            f"""
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
            """,
            (
                nieuwe_data['auteur'],
                nieuwe_data['beschrijving'],
                nieuwe_data['is_uitgeleend'],
                nieuwe_data['isbn'],
                nieuwe_data['kaft_foto_url'],
                nieuwe_data['publicatiedatum'],
                nieuwe_data['titel'],
                nieuwe_data['uitgeleend_datum'],
                nieuwe_data['uitgeleend_max_tot'],
                boek_id
            )
        )
        if cursor.rowcount == 0:
            raise BoekNietGevondenException("Boek niet gevonden voor update")
        self.db_connection.commit()
        return dict(id=boek_id, **nieuwe_data)

class BoekService:
    def __init__(self, boek_repository=None):
        self.repo = boek_repository or BoekRepository()

    def update_boek(self, boek_id, update_data):
        bestaande_boek = self.repo.get_boek_by_id(boek_id)
        if bestaande_boek is None:
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden")
        return self.repo.update_boek(bestaande_boek, update_data)
