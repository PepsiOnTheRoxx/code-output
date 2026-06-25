from src.services.seederdummyboeken_exceptions import (
    BoekSeederDatabaseError,
    BoekSeederAlreadySeededError
)

class BoekSeeder:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def seed(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM boeken")
            result = cursor.fetchone()
            count = result[0] if result else 0
            if count >= 5:
                raise BoekSeederAlreadySeededError("Database already contains minimum number of boeken.")
            dummy_boeken = [
                ("Het Diner", "Herman Koch", "9789023454795", 2009),
                ("De donkere kamer van Damokles", "Willem Frederik Hermans", "9789023423654", 1958),
                ("Joe Speedboot", "Tommy Wieringa", "9789023441245", 2005),
                ("Max Havelaar", "Multatuli", "9789028201158", 1860),
                ("De ontdekking van de hemel", "Harry Mulisch", "9789023419961", 1992)
            ]
            for boek in dummy_boeken:
                cursor.execute(
                    "INSERT INTO boeken (titel, auteur, isbn, jaar) VALUES (?, ?, ?, ?)",
                    boek
                )
            self.db_connection.commit()
        except BoekSeederAlreadySeededError:
            raise
        except Exception as e:
            raise BoekSeederDatabaseError("Database error tijdens seeden: {}".format(str(e)))
