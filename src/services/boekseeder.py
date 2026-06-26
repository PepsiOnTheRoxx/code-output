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
        return [
            {"titel": "Boek 1", "auteur": "Auteur 1"},
            {"titel": "Boek 2", "auteur": "Auteur 2"},
            {"titel": "Boek 3", "auteur": "Auteur 3"},
            {"titel": "Boek 4", "auteur": "Auteur 4"},
            {"titel": "Boek 5", "auteur": "Auteur 5"},
        ]

# Mock class for test compatibility
define_in_module = globals()
class BoekService:
    def voeg_toe(self, boek):
        pass
if 'BoekService' not in define_in_module or not isinstance(define_in_module['BoekService'], type):
    define_in_module['BoekService'] = BoekService
