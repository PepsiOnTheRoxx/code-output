from src.services.databaseseeder_exceptions import DatabaseSeederSeedError

class DatabaseSeeder:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def seed_books(self):
        cursor = self.db_connection.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM books")
            count = cursor.fetchone()[0]
            if count > 0:
                return

            dummy_books = [
                ("Het Gouden Ei", "Tim Krabbé", "Thriller", 1984),
                ("De Avonden", "Gerard Reve", "Roman", 1947),
                ("Max Havelaar", "Multatuli", "Historisch", 1860),
                ("Turks Fruit", "Jan Wolkers", "Roman", 1969),
                ("Hersenschimmen", "J. Bernlef", "Roman", 1984)
            ]
            for title, author, genre, year in dummy_books:
                cursor.execute(
                    "INSERT INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)",
                    (title, author, genre, year)
                )
            self.db_connection.commit()
        except Exception as e:
            self.db_connection.rollback()
            raise DatabaseSeederSeedError(str(e))
        finally:
            cursor.close()
