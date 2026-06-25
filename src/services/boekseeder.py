from src.services.boekseeder_exceptions import BoekSeederException

class BoekSeeder:
    def __init__(self, service):
        self.service = service

    def seed(self):
        boeken = [
            {"titel": "De Ontdekking van de Hemel", "auteur": "Harry Mulisch", "isbn": "9789023431231"},
            {"titel": "De donkere kamer van Damokles", "auteur": "W.F. Hermans", "isbn": "9789023451235"},
            {"titel": "Het Diner", "auteur": "Herman Koch", "isbn": "9789041415912"},
            {"titel": "Turks Fruit", "auteur": "Jan Wolkers", "isbn": "9789023425656"},
            {"titel": "Nooit meer slapen", "auteur": "W.F. Hermans", "isbn": "9789020413236"},
            {"titel": "Max Havelaar", "auteur": "Multatuli", "isbn": "9789020410396"}
        ]
        try:
            for boek in boeken:
                self.service.voeg_boek_toe(boek)
        except Exception as ex:
            raise BoekSeederException(str(ex))
        return None
