from src.services.boekseeder_exceptions import DatabaseCreationError, DummyBooksInsertionError

class BoekSeeder:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def seed(self):
        try:
            with self.db_connection.cursor() as cursor:
                try:
                    # Check and create boeken table if needed
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='boeken';")
                    tables = cursor.fetchall()
                    if not tables:
                        try:
                            cursor.execute(
                                "CREATE TABLE IF NOT EXISTS boeken (id INTEGER PRIMARY KEY AUTOINCREMENT, titel TEXT, auteur TEXT, jaar INTEGER);"
                            )
                        except Exception as ex:
                            raise DatabaseCreationError("Fout bij aanmaken van boeken-tabel: " + str(ex))
                except Exception as ex:
                    raise DatabaseCreationError(str(ex))
                # Check if boeken table is empty
                try:
                    cursor.execute("SELECT COUNT(*) FROM boeken;")
                    result = cursor.fetchall()
                    num_books = result[0][0] if result and result[0] else 0
                except Exception as ex:
                    raise DummyBooksInsertionError("Fout bij ophalen aantal boeken: " + str(ex))
                if num_books == 0:
                    dummy_boeken = [
                        ('Dummy Boek 1', 'Auteur 1', 2001),
                        ('Dummy Boek 2', 'Auteur 2', 2002),
                        ('Dummy Boek 3', 'Auteur 3', 2003),
                        ('Dummy Boek 4', 'Auteur 4', 2004),
                        ('Dummy Boek 5', 'Auteur 5', 2005),
                    ]
                    for boek in dummy_boeken:
                        try:
                            cursor.execute(
                                "INSERT INTO boeken (titel, auteur, jaar) VALUES (?, ?, ?);",
                                boek
                            )
                        except Exception as ex:
                            raise DummyBooksInsertionError("Fout bij invoegen van dummy-boeken: " + str(ex))
                    try:
                        self.db_connection.commit()
                    except Exception as ex:
                        raise DummyBooksInsertionError("Fout bij committen van dummy-boeken: " + str(ex))
        except DummyBooksInsertionError:
            raise
        except DatabaseCreationError:
            raise
