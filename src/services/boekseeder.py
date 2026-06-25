from src.services.boekseeder_exceptions import DatabaseSeedError

def get_db():
    # Deze functie wordt alleen tijdens runtime aangeroepen, voor de tests wordt het gemockt.
    # Voorkom importfout door geen import van niet-bestaande module src.db
    # In productie moet deze functie vervangen/uitgebreid worden naargelang het echte DB-object
    raise NotImplementedError("Er is geen db-module. get_db() moet gemockt worden in tests.")

class Boek:
    def __init__(self, titel, auteur, jaar):
        self.titel = titel
        self.auteur = auteur
        self.jaar = jaar

class BoekSeeder:
    DUMMY_BOEKEN = [
        {"titel": "Het geheim van de schrijver", "auteur": "Renate Dorrestein", "jaar": 2000},
        {"titel": "De ontdekking van de hemel", "auteur": "Harry Mulisch", "jaar": 1992},
        {"titel": "Max Havelaar", "auteur": "Multatuli", "jaar": 1860},
        {"titel": "Turks Fruit", "auteur": "Jan Wolkers", "jaar": 1969},
        {"titel": "Publieke Werken", "auteur": "Thomas Rosenboom", "jaar": 1999},
    ]

    def __init__(self, db_instance=None):
        if db_instance is not None:
            self.db = db_instance
        else:
            self.db = get_db()

    def seed(self):
        session = self.db.session
        try:
            count = session.query().count()
            if count > 0:
                return
            for boek in self.DUMMY_BOEKEN:
                session.add(boek)
            session.commit()
        except Exception as exc:
            session.rollback()
            raise DatabaseSeedError(f"Database error during seeding: {exc}")
