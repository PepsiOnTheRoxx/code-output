from src.services.boekseeder_exceptions import BoekSeederDatabaseException

class BoekSeeder:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def seed(self):
        boeken = [
            ("Titel 1", "Auteur 1", 2020, "9781234567890"),
            ("Titel 2", "Auteur 2", 2021, "9781234567891"),
            ("Titel 3", "Auteur 3", 2019, "9781234567892"),
            ("Titel 4", "Auteur 4", 2018, "9781234567893"),
            ("Titel 5", "Auteur 5", 2022, "9781234567894"),
        ]
        cursor = self.db_connection.cursor()
        inserted = 0
        try:
            for boek in boeken:
                cursor.execute(
                    "INSERT INTO boeken (titel, auteur, jaar, isbn) VALUES (?, ?, ?, ?)",
                    boek
                )
                inserted += 1
            self.db_connection.commit()
        except Exception as e:
            self.db_connection.rollback()
            raise BoekSeederDatabaseException(str(e))
