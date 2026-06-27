from .boekseeder_exceptions import (
    BoekSeederException,
    BoekSeederInvalidBookCountException,
    BoekSeederServiceException,
)

class BoekSeeder:
    def __init__(self, boek_service):
        self.boek_service = boek_service

    def seed(self):
        dummy_boeken = self._maak_dummy_boeken()
        if len(dummy_boeken) < 5:
            raise BoekSeederInvalidBookCountException(
                "Er moeten minimaal vijf boeken worden toegevoegd.")
        try:
            for boek in dummy_boeken:
                self.boek_service.voeg_toe(boek)
        except Exception as e:
            raise BoekSeederServiceException(
                f"Fout bij toevoegen van boeken: {str(e)}") from e

    def _maak_dummy_boeken(self):
        # Semua velden uit het schema:
        return [
            {
                "titel": "Boek 1",
                "auteur": "Auteur 1",
                "beschrijving": "Beschrijving 1",
                "isbn": "9780000000001",
                "publicatiedatum": "2020-01-01",
                "kaft_foto_url": "http://example.com/boek1.jpg",
                "is_uitgeleend": 0,
                "uitgeleend_datum": None,
                "uitgeleend_max_tot": None,
            },
            {
                "titel": "Boek 2",
                "auteur": "Auteur 2",
                "beschrijving": "Beschrijving 2",
                "isbn": "9780000000002",
                "publicatiedatum": "2021-02-02",
                "kaft_foto_url": "http://example.com/boek2.jpg",
                "is_uitgeleend": 0,
                "uitgeleend_datum": None,
                "uitgeleend_max_tot": None,
            },
            {
                "titel": "Boek 3",
                "auteur": "Auteur 3",
                "beschrijving": "Beschrijving 3",
                "isbn": "9780000000003",
                "publicatiedatum": "2022-03-03",
                "kaft_foto_url": "http://example.com/boek3.jpg",
                "is_uitgeleend": 0,
                "uitgeleend_datum": None,
                "uitgeleend_max_tot": None,
            },
            {
                "titel": "Boek 4",
                "auteur": "Auteur 4",
                "beschrijving": "Beschrijving 4",
                "isbn": "9780000000004",
                "publicatiedatum": "2023-04-04",
                "kaft_foto_url": "http://example.com/boek4.jpg",
                "is_uitgeleend": 0,
                "uitgeleend_datum": None,
                "uitgeleend_max_tot": None,
            },
            {
                "titel": "Boek 5",
                "auteur": "Auteur 5",
                "beschrijving": "Beschrijving 5",
                "isbn": "9780000000005",
                "publicatiedatum": "2024-05-05",
                "kaft_foto_url": "http://example.com/boek5.jpg",
                "is_uitgeleend": 0,
                "uitgeleend_datum": None,
                "uitgeleend_max_tot": None,
            },
        ]

# Mock class for test compatibility
define_in_module = globals()
class BoekService:
    def voeg_toe(self, boek):
        pass
if 'BoekService' not in define_in_module or not isinstance(define_in_module['BoekService'], type):
    define_in_module['BoekService'] = BoekService
