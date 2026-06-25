from database import get_connection
from src.services.boekseeder_exceptions import (
    BoekSeederException,
    BoekSeederDatabaseError,
    BoekSeederServiceUnavailable,
    BoekSeederInvalidDataError,
    BoekSeederInsufficientRecordsError
)

dummy_boeken = [
    {"titel": "Boek 1", "auteur": "Auteur 1"},
    {"titel": "Boek 2", "auteur": "Auteur 2"},
    {"titel": "Boek 3", "auteur": "Auteur 3"},
    {"titel": "Boek 4", "auteur": "Auteur 4"},
    {"titel": "Boek 5", "auteur": "Auteur 5"},
]

class BoekSeedingException(Exception):
    pass

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create(self, boek_data):
        try:
            cursor = self.db_connection.cursor()
            if "titel" not in boek_data:
                raise BoekSeederInvalidDataError("Titel ontbreekt")
            auteur = boek_data.get("auteur", "")
            cursor.execute(
                "INSERT INTO boek (titel, auteur) VALUES (?, ?)",
                (boek_data["titel"], auteur)
            )
            self.db_connection.commit()
        except Exception as exc:
            raise BoekSeederDatabaseError(str(exc))

class BoekSeeder:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection or get_connection()
        self.boek_service = BoekService(self.db_connection)

    def run(self):
        records_inserted = 0
        try:
            for boek in dummy_boeken:
                try:
                    self.boek_service.create(boek)
                    records_inserted += 1
                except BoekSeederException as exc:
                    raise
                except Exception as exc:
                    raise BoekSeederException(str(exc))
            if records_inserted < 5:
                raise BoekSeederInsufficientRecordsError("Minder dan 5 Boek records gecreëerd.")
        except Exception as exc:
            raise BoekSeedingException(str(exc))