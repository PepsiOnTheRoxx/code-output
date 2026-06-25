from src.services.boekread_exceptions import BoekNietGevondenException, DatabaseFoutException

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_boek(self, boek_id):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, titel, auteur, jaar FROM boeken WHERE id = %s", (boek_id,)
                )
                row = cursor.fetchone()
                if row is None:
                    raise BoekNietGevondenException()
                return {
                    "id": row[0],
                    "titel": row[1],
                    "auteur": row[2],
                    "jaar": row[3]
                }
        except BoekNietGevondenException:
            raise
        except Exception:
            raise DatabaseFoutException()

    def get_all_boeken(self):
        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, titel, auteur, jaar FROM boeken"
                )
                rows = cursor.fetchall()
                return [
                    {"id": row[0], "titel": row[1], "auteur": row[2], "jaar": row[3]}
                    for row in rows
                ]
        except Exception:
            raise DatabaseFoutException()