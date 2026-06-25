from src.frontend.catalogusfrontend_exceptions import CatalogusPageLoadError, BoekAPIFailure

class CatalogusPage:
    def __init__(self, db_connection, boek_api):
        self.db_connection = db_connection
        self.boek_api = boek_api
        self._ensure_tables()

    def _ensure_tables(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS navigatie (
                    id INTEGER PRIMARY KEY,
                    boek_id INTEGER,
                    actie TEXT
                )
            """)
            self.db_connection.commit()
        except Exception as e:
            raise CatalogusPageLoadError("Fout bij het aanmaken van de navigatietabel") from e

    def laad_catalogus(self):
        try:
            boeken = self.boek_api.haal_alle_boeken()
            if boeken is None:
                raise BoekAPIFailure("BoekAPI gaf geen resultaten terug")
            return boeken
        except BoekAPIFailure:
            raise
        except Exception as e:
            raise CatalogusPageLoadError("Fout bij het laden van de catalogus") from e

    def navigeer_naar_boek_detail(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT INTO navigatie (boek_id, actie) VALUES (?, ?)",
                (boek_id, 'detail')
            )
            self.db_connection.commit()
        except Exception as e:
            raise CatalogusPageLoadError("Navigatie naar detailpagina mislukt") from e

    def navigeer_naar_nieuw_boek(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT INTO navigatie (boek_id, actie) VALUES (?, ?)",
                (None, 'nieuw')
            )
            self.db_connection.commit()
        except Exception as e:
            raise CatalogusPageLoadError("Navigatie naar nieuw-boekpagina mislukt") from e

    def navigeer_naar_boek_aanpassen(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT INTO navigatie (boek_id, actie) VALUES (?, ?)",
                (boek_id, 'aanpassen')
            )
            self.db_connection.commit()
        except Exception as e:
            raise CatalogusPageLoadError("Navigatie naar aanpaspagina mislukt") from e