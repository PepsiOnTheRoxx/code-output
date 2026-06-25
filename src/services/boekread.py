from src.services.boekread_exceptions import BoekNietGevondenException, DatabaseFoutException

class BoekReadService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def haal_alle_boeken_op(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, titel, auteur FROM boeken")
            rows = cursor.fetchall()
            return [{'id': r[0], 'titel': r[1], 'auteur': r[2]} for r in rows]
        except Exception:
            raise DatabaseFoutException()

    def haal_boek_op_id(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT id, titel, auteur FROM boeken WHERE id = ?", (boek_id,))
            row = cursor.fetchone()
            if row is None:
                raise BoekNietGevondenException()
            return {'id': row[0], 'titel': row[1], 'auteur': row[2]}
        except BoekNietGevondenException:
            raise
        except Exception:
            raise DatabaseFoutException()