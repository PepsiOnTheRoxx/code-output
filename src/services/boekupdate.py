from database import get_connection
from src.services.boekupdate_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

class BoekService:
    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection

    def get_boek_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, titel FROM boeken WHERE id = ?", (boek_id,))
        row = cursor.fetchone()
        if row:
            boek = type('Boek', (object,), {})()
            boek.id = row[0]
            boek.titel = row[1]
            return boek
        return None

    def save_boek(self, boek):
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE boeken SET titel = ? WHERE id = ?", (boek.titel, boek.id))
        self.db_connection.commit()

    def update_boek(self, boek_id, update_data):
        boek = self.get_boek_by_id(boek_id)
        if boek is None:
            raise BoekNietGevondenException(f'Boek met id {boek_id} niet gevonden')
        if "titel" in update_data:
            if not update_data["titel"]:
                raise OngeldigeBoekDataException("Titel mag niet leeg zijn")
            boek.titel = update_data["titel"]
        self.save_boek(boek)
        return boek