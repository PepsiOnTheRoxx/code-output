import os
import sqlite3
from database_exceptions import DatabaseInitializationError

DB_PATH = os.path.join(os.path.dirname(__file__), 'bibliotheek.db')

CREATE_BOEK_TABLE = (
    "CREATE TABLE IF NOT EXISTS Boek "
    "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "titel TEXT, "
    "auteur TEXT, "
    "isbn TEXT, "
    "uitgever TEXT, "
    "jaar INTEGER, "
    "categorie TEXT, "
    "taal TEXT, "
    "pagina_count INTEGER, "
    "samenvatting TEXT)"
)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(CREATE_BOEK_TABLE)
        conn.commit()
    except Exception as e:
        raise DatabaseInitializationError(str(e))
    finally:
        if conn:
            conn.close()

class DatabaseSetup:
    def __init__(self, connection):
        self.conn = connection

    def initialize_database(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(CREATE_BOEK_TABLE)
            self.conn.commit()
        except Exception as e:
            raise DatabaseInitializationError(str(e))

# Utility function for tests/consumers to validate Boek table declaration
def get_boek_columns():
    # Returns ordered list of the Boek table column names
    return [
        'id',
        'titel',
        'auteur',
        'isbn',
        'uitgever',
        'jaar',
        'categorie',
        'taal',
        'pagina_count',
        'samenvatting'
    ]