from src.services.boekread_exceptions import BoekNietGevondenException

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def haal_boek_op(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, titel, auteur FROM boeken WHERE id=?;", (boek_id,))
        row = cursor.fetchone()
        if row is None:
            raise BoekNietGevondenException()
        return {
            "id": row[0],
            "titel": row[1],
            "auteur": row[2]
        }

    def haal_alle_boeken(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, titel, auteur FROM boeken;")
        rows = cursor.fetchall()
        boeken = []
        for row in rows:
            boeken.append({
                "id": row[0],
                "titel": row[1],
                "auteur": row[2]
            })
        return boeken