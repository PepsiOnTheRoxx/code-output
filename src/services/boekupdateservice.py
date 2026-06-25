from src.services.boekupdateservice_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

class BoekUpdateService:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def update_boek(self, boek_id, nieuwe_data):
        vereiste_keys = {'titel', 'auteur', 'jaar'}
        if not isinstance(nieuwe_data, dict) or set(nieuwe_data.keys()) != vereiste_keys:
            raise OngeldigeBoekDataException("Ongeldige data: ontbrekende of extra velden.")

        titel = nieuwe_data.get('titel')
        auteur = nieuwe_data.get('auteur')
        jaar = nieuwe_data.get('jaar')

        if not isinstance(titel, str) or not isinstance(auteur, str) or not isinstance(jaar, int):
            raise OngeldigeBoekDataException("Ongeldige data: verkeerde types of lege waarden.")

        cursor = None
        try:
            cursor = self.db_conn.cursor()
            sql = "UPDATE boeken SET titel=?, auteur=?, jaar=? WHERE id=?"
            params = (titel, auteur, jaar, boek_id)
            cursor.execute(sql, params)

            if cursor.rowcount == 0:
                raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden.")

            self.db_conn.commit()
        except (BoekNietGevondenException, OngeldigeBoekDataException):
            raise
        except Exception as e:
            self.db_conn.rollback()
            raise
        finally:
            if cursor is not None:
                cursor.close()