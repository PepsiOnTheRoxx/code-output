from src.services.boekupdate_exceptions import (
    BoekNietGevondenException,
    OngeldigeBoekDataException,
)

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def update_boek(self, boek_id, boek_data):
        verplichte_velden = ["titel", "auteur", "jaar", "genre", "isbn"]
        if not isinstance(boek_data, dict) or not all(v in boek_data for v in verplichte_velden):
            raise OngeldigeBoekDataException("Ontbrekende of ongeldige boekvelden")

        try:
            cursor = self.db_connection.cursor()
            query = (
                "UPDATE boek SET "
                "titel = ?, auteur = ?, jaar = ?, genre = ?, isbn = ? "
                "WHERE id = ?"
            )
            params = (
                boek_data["titel"],
                boek_data["auteur"],
                boek_data["jaar"],
                boek_data["genre"],
                boek_data["isbn"],
                boek_id,
            )
            cursor.execute(query, params)
            if cursor.rowcount == 0:
                raise BoekNietGevondenException("Boek niet gevonden voor update")
            self.db_connection.commit()
        except BoekNietGevondenException:
            raise
        except Exception as ex:
            self.db_connection.rollback()
            raise ex