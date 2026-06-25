from src.services.boekupdate_exceptions import BoekNotFoundException, BoekUpdateValidationException

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def update_boek(self, boek_id, nieuwe_data):
        verplichte_velden = ["titel", "auteur"]
        for veld in verplichte_velden:
            if veld not in nieuwe_data:
                raise BoekUpdateValidationException("Verplicht veld ontbreekt: " + veld)
        cursor = self.db_connection.cursor()
        try:
            sql = "UPDATE boeken SET titel = ?, auteur = ? WHERE id = ?"
            waarden = (
                nieuwe_data["titel"],
                nieuwe_data["auteur"],
                boek_id
            )
            cursor.execute(sql, waarden)
            if cursor.rowcount == 0:
                raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden")
            self.db_connection.commit()
        except Exception as ex:
            self.db_connection.rollback()
            raise ex
        finally:
            cursor.close()
