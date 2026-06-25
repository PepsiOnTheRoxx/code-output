from src.services.boekseeder_exceptions import (
    BoekSeederException,
    BoekSeederDatabaseError,
    BoekSeederServiceUnavailable,
    BoekSeederInvalidDataError,
    BoekSeederInsufficientRecordsError,
    BoekSeedingException
)

# Dummy data met ALLE vereiste velden uit het schema:
dummy_boeken = [
    {
        "titel": f"Boek {i+1}",
        "auteur": f"Auteur {i+1}",
        "beschrijving": f"Beschrijving voor boek {i+1}",
        "isbn": f"978000000000{i}",
        "kaft_foto_url": "https://example.com/kaft.jpg",
        "publicatiedatum": "2023-01-01",
        "is_uitgeleend": False,
        "uitgeleend_datum": None,
        "uitgeleend_max_tot": None
    }
    for i in range(5)
]

class BoekService:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection

    def create(self, boek_data):
        if "titel" not in boek_data:
            raise BoekSeederInvalidDataError("Titel ontbreekt")
        return True

class BoekSeeder:
    def __init__(self, db_connection=None):
        self.db_connection = db_connection
        self.boek_service = BoekService(self.db_connection)

    def run(self):
        records_inserted = 0
        for boek in dummy_boeken:
            try:
                self.boek_service.create(boek)
                records_inserted += 1
            except BoekSeederException:
                raise
            except Exception as exc:
                if type(exc).__name__ == 'Exception':
                    raise BoekSeedingException(str(exc))
                raise
        if records_inserted < 5:
            raise BoekSeederInsufficientRecordsError("Minder dan 5 Boek records gecreëerd.")
