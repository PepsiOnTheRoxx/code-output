from src.frontend.boekaanpassenfrontend_exceptions import BoekNietGevondenException, BewerkenMisluktException

class BoekAanpassenPage:
    def __init__(self, db_connection, boek_api):
        self.db_connection = db_connection
        self.boek_api = boek_api

    def get_boek(self, boek_id):
        boek = self.boek_api.get_boek(boek_id)
        if not boek:
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden")
        return boek

    def get_edit_form(self, boek_id):
        boek = self.get_boek(boek_id)
        return {
            "titel": boek.get("titel", ""),
            "auteur": boek.get("auteur", ""),
            "isbn": boek.get("isbn", ""),
            "jaar": boek.get("jaar", ""),
            "omschrijving": boek.get("omschrijving", ""),
        }

    def handle_submit(self, boek_id, data):
        try:
            success = self.boek_api.update_boek(boek_id, data)
            if not success:
                raise BewerkenMisluktException(f"Aanpassen van boek met id {boek_id} mislukt")
            return {
                "redirect": f"/boeken/{boek_id}"
            }
        except Exception as e:
            raise BewerkenMisluktException(str(e))

    def handle_cancel(self):
        return {
            "redirect": "/catalogus"
        }