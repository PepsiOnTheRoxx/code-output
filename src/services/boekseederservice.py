import sqlite3
from src.services.boekseederservice_exceptions import DatabaseInitialisatieFout

class BoekSeeder:
    _db_path = "boeken.db"

    def initialiseer_database(self):
        try:
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS boeken (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titel TEXT NOT NULL,
                    auteur TEXT NOT NULL,
                    isbn TEXT NOT NULL,
                    jaar INTEGER NOT NULL
                )
                """
            )
            conn.commit()
            conn.close()
        except Exception as e:
            raise DatabaseInitialisatieFout(str(e))

    def seed(self):
        try:
            conn = sqlite3.connect(self._db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM boeken")
            count = cursor.fetchone()[0]
            if count > 0:
                conn.close()
                return
            boeken = self._genereer_dummy_boeken()
            cursor.executemany(
                "INSERT INTO boeken (titel, auteur, isbn, jaar) VALUES (?, ?, ?, ?)",
                [(b["titel"], b["auteur"], b["isbn"], b["jaar"]) for b in boeken]
            )
            conn.commit()
            conn.close()
        except Exception as e:
            raise DatabaseInitialisatieFout(str(e))

    @staticmethod
    def _genereer_dummy_boeken():
        return [
            {"titel": "Boek 1", "auteur": "Auteur 1", "isbn": "ISBN1", "jaar": 2001},
            {"titel": "Boek 2", "auteur": "Auteur 2", "isbn": "ISBN2", "jaar": 2002},
            {"titel": "Boek 3", "auteur": "Auteur 3", "isbn": "ISBN3", "jaar": 2003},
            {"titel": "Boek 4", "auteur": "Auteur 4", "isbn": "ISBN4", "jaar": 2004},
            {"titel": "Boek 5", "auteur": "Auteur 5", "isbn": "ISBN5", "jaar": 2005},
        ]