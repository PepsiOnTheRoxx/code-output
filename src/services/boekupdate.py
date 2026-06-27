from database import get_connection
from src.services.boekupdate_exceptions import (
    BoekNietGevondenException,
    BoekUpdateValidatieException,
)

class BoekService:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection if db_connection else get_connection()

    def get_boek_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, titel, auteur FROM boek WHERE id = ?", (boek_id,))
        row = cursor.fetchone()
        if row:
            return Boek(row[0], row[1], row[2])
        return None

    def save_boek(self, boek):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "UPDATE boek SET titel = ?, auteur = ? WHERE id = ?",
            (boek.titel, boek.auteur, boek.id)
        )
        self.db_connection.commit()
        return boek

    def update_boek(self, boek_id, nieuwe_data):
        boek = self.get_boek_by_id(boek_id)
        if not boek:
            raise BoekNietGevondenException("Boek met id {} niet gevonden".format(boek_id))
        try:
            boek.update(nieuwe_data)
        except BoekUpdateValidatieException:
            raise
        except Exception as e:
            raise
        try:
            return self.save_boek(boek)
        except Exception as e:
            raise

class Boek:
    def __init__(self, id, titel, auteur):
        self.id = id
        self.titel = titel
        self.auteur = auteur

    def update(self, data):
        if "titel" in data:
            if not isinstance(data["titel"], str) or not data["titel"].strip():
                raise BoekUpdateValidatieException("Titel mag niet leeg zijn")
            self.titel = data["titel"]
        if "auteur" in data:
            if not isinstance(data["auteur"], str) or not data["auteur"].strip():
                raise BoekUpdateValidatieException("Auteur mag niet leeg zijn")
            self.auteur = data["auteur"]
