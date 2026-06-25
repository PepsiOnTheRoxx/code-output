from src.services.boekseeder_exceptions import BoekSeederException

class BoekSeeder:
    def __init__(self, service):
        self.service = service

    def seed(self):
        boeken = [
            {"titel": "De Ontdekking van de Hemel", "auteur": "Harry Mulisch"},
            {"titel": "De donkere kamer van Damokles", "auteur": "W.F. Hermans"},
            {"titel": "Het Diner", "auteur": "Herman Koch"},
            {"titel": "Turks Fruit", "auteur": "Jan Wolkers"},
            {"titel": "Nooit meer slapen", "auteur": "W.F. Hermans"},
            {"titel": "Max Havelaar", "auteur": "Multatuli"}
        ]
        try:
            for boek in boeken:
                self.service.voeg_boek_toe(boek)
        except Exception as ex:
            raise BoekSeederException(str(ex))
        return None