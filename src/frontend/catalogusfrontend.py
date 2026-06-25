from src.frontend.catalogusfrontend_exceptions import (
    BoekNietGevondenException,
    DatabaseFoutException,
    BoekToevoegenException,
    BoekAanpassenException
)

class CatalogusFrontend:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_catalogus(self):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT id, titel, auteur, kaft_foto_url, uitleen_status FROM boeken"
            )
            boeken = cursor.fetchall()
            resultaat = []
            for boek in boeken:
                resultaat.append({
                    "id": boek[0],
                    "titel": boek[1],
                    "auteur": boek[2],
                    "kaft_foto_url": boek[3],
                    "uitleen_status": boek[4]
                })
            return resultaat
        except Exception as e:
            raise DatabaseFoutException("Fout bij laden van catalogus") from e

    def get_boek_detail(self, boek_id):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT id, titel, auteur, kaft_foto_url, uitleen_status FROM boeken WHERE id = ?",
                (boek_id,)
            )
            boek = cursor.fetchone()
            if not boek:
                raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden")
            return {
                "id": boek[0],
                "titel": boek[1],
                "auteur": boek[2],
                "kaft_foto_url": boek[3],
                "uitleen_status": boek[4]
            }
        except BoekNietGevondenException:
            raise
        except Exception as e:
            raise DatabaseFoutException("Fout bij ophalen van boekdetail") from e

    def voeg_boek_toe(self, titel, auteur, kaft_foto_url, uitleen_status):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "INSERT INTO boeken (titel, auteur, kaft_foto_url, uitleen_status) VALUES (?, ?, ?, ?)",
                (titel, auteur, kaft_foto_url, uitleen_status)
            )
            self.db_connection.commit()
            return cursor.lastrowid
        except Exception as e:
            raise BoekToevoegenException("Fout bij toevoegen van boek") from e

    def pas_boek_aan(self, boek_id, titel=None, auteur=None, kaft_foto_url=None, uitleen_status=None):
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(
                "SELECT id FROM boeken WHERE id = ?",
                (boek_id,)
            )
            if not cursor.fetchone():
                raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden")

            updates = []
            params = []
            if titel is not None:
                updates.append("titel = ?")
                params.append(titel)
            if auteur is not None:
                updates.append("auteur = ?")
                params.append(auteur)
            if kaft_foto_url is not None:
                updates.append("kaft_foto_url = ?")
                params.append(kaft_foto_url)
            if uitleen_status is not None:
                updates.append("uitleen_status = ?")
                params.append(uitleen_status)

            if updates:
                params.append(boek_id)
                sql = "UPDATE boeken SET " + ", ".join(updates) + " WHERE id = ?"
                cursor.execute(sql, params)
                self.db_connection.commit()
            else:
                raise BoekAanpassenException("Geen velden om aan te passen opgegeven")
        except (BoekNietGevondenException, BoekAanpassenException):
            raise
        except Exception as e:
            raise BoekAanpassenException("Fout bij aanpassen van boek") from e

    def navigeer_naar_detail(self, boek_id):
        try:
            boek_detail = self.get_boek_detail(boek_id)
            # Hypothetisch: Return het detail data-struct of URL
            return boek_detail
        except BoekNietGevondenException:
            raise
        except Exception as e:
            raise DatabaseFoutException("Fout bij navigatie naar detailpagina") from e

    def navigeer_naar_toevoegen(self):
        # Hypothetisch: Return path of component-naam voor toevoegen
        return "catalogus_toevoegen_pagina"

    def navigeer_naar_aanpassen(self, boek_id):
        try:
            boek_detail = self.get_boek_detail(boek_id)
            # Hypothetisch: Return aanpas-pagina data-struct of URL
            return boek_detail
        except BoekNietGevondenException:
            raise
        except Exception as e:
            raise DatabaseFoutException("Fout bij navigatie naar aanpaspagina") from e