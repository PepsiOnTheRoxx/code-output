import os
import sqlite3
from database_exceptions import DatabaseInitialisatieFout

DB_PATH = os.path.join(os.path.dirname(__file__), 'bibliotheek.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS Boek "
            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "titel TEXT NOT NULL, "
            "auteur TEXT NOT NULL, "
            "isbn TEXT NOT NULL, "
            "uitgever TEXT NOT NULL, "
            "publicatiejaar INTEGER, "
            "genre TEXT, "
            "taal TEXT, "
            "paginas INTEGER, "
            "beschikbaar INTEGER DEFAULT 1)"
        )
        conn.commit()
        cursor.close()
    except Exception as e:
        cursor.close()
        raise DatabaseInitialisatieFout(str(e))

class DatabaseSetup:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def initialiseer_database(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Boek "
                "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "titel TEXT NOT NULL, "
                "auteur TEXT NOT NULL, "
                "isbn TEXT NOT NULL, "
                "uitgever TEXT NOT NULL, "
                "publicatiejaar INTEGER, "
                "genre TEXT, "
                "taal TEXT, "
                "paginas INTEGER, "
                "beschikbaar INTEGER DEFAULT 1)"
            )
            self.db_connection.commit()
            cursor.close()
        except Exception as e:
            cursor.close()
            raise DatabaseInitialisatieFout(str(e))