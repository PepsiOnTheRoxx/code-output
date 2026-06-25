from src.services.boekupdate_exceptions import (
    BoekNietGevondenException,
    OngeldigeBoekDataException,
)
from database import get_connection


class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_boek_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, titel, auteur FROM boek WHERE id = ?", (boek_id,))
        row = cursor.fetchone()
        if row:
            return {'id': row[0], 'titel': row[1], 'auteur': row[2]}
        return None

    def update_boek(self, bestaande_boek, update_data):
        boek_id = bestaande_boek['id']
        titel = update_data.get('titel', bestaande_boek.get('titel'))
        auteur = update_data.get('auteur', bestaande_boek.get('auteur'))

        if not titel or not isinstance(titel, str):
            raise OngeldigeBoekDataException('Titel is verplicht en mag niet leeg zijn')

        cursor = self.db_connection.cursor()
        cursor.execute(
            "UPDATE boek SET titel = ?, auteur = ? WHERE id = ?",
            (titel, auteur, boek_id)
        )
        if cursor.rowcount == 0:
            raise BoekNietGevondenException("Boek niet gevonden voor update")
        self.db_connection.commit()
        return {'id': boek_id, 'titel': titel, 'auteur': auteur}


class BoekService:
    def __init__(self, boek_repository):
        self.repo = boek_repository

    def update_boek(self, boek_id, update_data):
        bestaande_boek = self.repo.get_boek_by_id(boek_id)
        if bestaande_boek is None:
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden")
        return self.repo.update_boek(bestaande_boek, update_data)