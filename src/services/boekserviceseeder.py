from src.services.boekserviceseeder_exceptions import (
    TableAlreadyExistsException,
    DatabaseSeedException,
)

MINIMUM_DUMMY_BOOKS = 5

class BoekServiceSeeder:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def create_and_seed_table(self):
        cursor = self.db_connection.cursor()
        try:
            try:
                cursor.execute(
                    """
                    CREATE TABLE Boek (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        titel TEXT NOT NULL,
                        auteur TEXT NOT NULL,
                        isbn TEXT NOT NULL,
                        publicatiejaar INTEGER NOT NULL,
                        genre TEXT NOT NULL
                    );
                    """
                )
            except Exception as e:
                if "already exists" in str(e).lower():
                    self.db_connection.rollback()
                    raise TableAlreadyExistsException("Boek tabel bestaat al")
                else:
                    self.db_connection.rollback()
                    raise

            dummy_boeken = [
                ("De Avonturen van Python", "Jan Jansen", "978-1234567890", 2021, "Educatief"),
                ("Slaap zacht, code kracht", "Lisa Smit", "978-2345678901", 2020, "Kinderboek"),
                ("AI voor beginners", "Mohammed El Idrissi", "978-3456789012", 2022, "Non-fictie"),
                ("Mysterie aan de Maas", "Eva van Dijk", "978-4567890123", 2019, "Thriller"),
                ("De verloren bytes", "Frits Bakker", "978-5678901234", 2023, "Sciencefiction"),
            ]

            while len(dummy_boeken) < MINIMUM_DUMMY_BOOKS:
                dummy_boeken.append(
                    ("Dummy Boek %d" % (len(dummy_boeken)+1), "Auteur X", "978-%d" % (len(dummy_boeken)+7)*10, 2015, "Onbekend")
                )

            for boek in dummy_boeken[:MINIMUM_DUMMY_BOOKS]:
                try:
                    cursor.execute(
                        "INSERT INTO Boek (titel, auteur, isbn, publicatiejaar, genre) VALUES (?, ?, ?, ?, ?);",
                        boek
                    )
                except Exception as e:
                    self.db_connection.rollback()
                    raise DatabaseSeedException("Fout bij toevoegen boek: %s" % str(e))

            self.db_connection.commit()

        except TableAlreadyExistsException:
            raise
        except DatabaseSeedException:
            raise
        except Exception as e:
            self.db_connection.rollback()
            raise