from src.frontend.boekdetailfrontend_exceptions import BoekNietGevondenException, BoekApiFoutException

class BoekDetailPage:
    def __init__(self, db_connection, boek_api):
        self.db_connection = db_connection
        self.boek_api = boek_api

    def get_boek_detail(self, boek_id):
        try:
            boek = self.boek_api.haal_boek_op(boek_id)
            uitleeninformatie = self._haal_uitleeninformatie_op(boek_id)
            detail = {
                "id": boek["id"],
                "titel": boek["titel"],
                "auteur": boek["auteur"],
                "jaar": boek["jaar"],
                "isbn": boek["isbn"],
                "categorie": boek["categorie"],
                "status": boek["status"],
                "uitleeninformatie": uitleeninformatie
            }
            return detail
        except KeyError:
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden.")
        except Exception as e:
            raise BoekApiFoutException(str(e))

    def _haal_uitleeninformatie_op(self, boek_id):
        cursor = self.db_connection.cursor()
        query = """
            SELECT l.id, l.lener, l.datum_uitleen, l.datum_terug
            FROM uitleen l
            WHERE l.boek_id = ?
            ORDER BY l.datum_uitleen DESC
            LIMIT 1
        """
        cursor.execute(query, (boek_id,))
        row = cursor.fetchone()
        if not row:
            return None
        uitleen = {
            "uitleen_id": row[0],
            "lener": row[1],
            "datum_uitleen": row[2],
            "datum_terug": row[3]
        }
        return uitleen

    def navigeer_naar_aanpassen(self, boek_id):
        # frontend stub, return next page route/state
        return {"route": f"/boeken/{boek_id}/aanpassen"}

    def navigeer_naar_catalogus(self):
        # frontend stub, return next page route/state
        return {"route": "/catalogus"}