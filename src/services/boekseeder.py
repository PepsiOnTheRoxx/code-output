from src.services.boekseeder_exceptions import BoekSeederDatabaseError
from database import get_connection

class BoekSeeder:
    DUMMY_BOEKEN = [
        {"titel": "Het geheim van de schrijver", "auteur": "Renate Dorrestein", "jaar": 2000},
        {"titel": "De ontdekking van de hemel", "auteur": "Harry Mulisch", "jaar": 1992},
        {"titel": "Max Havelaar", "auteur": "Multatuli", "jaar": 1860},
        {"titel": "Turks Fruit", "auteur": "Jan Wolkers", "jaar": 1969},
        {"titel": "Publieke Werken", "auteur": "Thomas Rosenboom", "jaar": 1999},
    ]

    def __init__(self, db_connection=None):
        if db_connection is None:
            self.db_connection = get_connection()
        else:
            self.db_connection = db_connection

    def seed(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM Boek")
            count = cursor.fetchone()[0]
            if count > 0:
                return
            for boek in self.DUMMY_BOEKEN:
                cursor.execute(
                    "INSERT INTO Boek (titel, auteur, jaar) VALUES (?, ?, ?)",
                    (boek["titel"], boek["auteur"], boek["jaar"]),
                )
            self.db_connection.commit()
        except Exception as exc:
            self.db_connection.rollback()
            raise BoekSeederDatabaseError(f"Fout bij seeden van boeken: {exc}")