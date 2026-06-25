from src.services.boekupdateservice_exceptions import (
    BoekNietGevondenException,
    OngeldigeBoekDataException,
    BoekUpdateMisluktException,
    BoekServiceDatabaseException,
)


class Boek:
    def __init__(self, id, titel, auteur, isbn):
        self.id = id
        self.titel = titel
        self.auteur = auteur
        self.isbn = isbn


class BoekRepository:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_boek_by_id(self, boek_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id, titel, auteur, isbn FROM boek WHERE id = ?", (boek_id,))
        row = cursor.fetchone()
        if row:
            return Boek(id=row[0], titel=row[1], auteur=row[2], isbn=row[3])
        return None

    def update_boek(self, boek):
        cursor = self.db_connection.cursor()
        cursor.execute(
            "UPDATE boek SET titel = ?, auteur = ?, isbn = ? WHERE id = ?",
            (boek.titel, boek.auteur, boek.isbn, boek.id),
        )
        self.db_connection.commit()


class BoekService:
    def __init__(self, repository):
        self.repository = repository

    def update_boek(self, boek_id, boek_data):
        oud_boek = self.repository.get_boek_by_id(boek_id)
        if oud_boek is None:
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden.")

        if not boek_data.get("titel") or not boek_data.get("auteur") or not boek_data.get("isbn"):
            raise OngeldigeBoekDataException("Titel, auteur en ISBN mogen niet leeg zijn.")

        nieuw_boek = Boek(
            id=boek_id,
            titel=boek_data["titel"],
            auteur=boek_data["auteur"],
            isbn=boek_data["isbn"],
        )

        try:
            self.repository.update_boek(nieuw_boek)
        except Exception as e:
            raise e