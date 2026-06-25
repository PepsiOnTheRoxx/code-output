from src.services.boekupdate_exceptions import BoekNietGevondenException, OngeldigeBoekDataException

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def update_boek(self, boek_id, boek_data):
        # Validatie van boek_data -- vereist: niet lege string voor 'titel', niet None en niet lege string voor 'auteur'
        if (
            not isinstance(boek_data, dict)
            or 'titel' not in boek_data or 'auteur' not in boek_data
            or not isinstance(boek_data['titel'], str) or not boek_data['titel'].strip()
            or boek_data['auteur'] is None or (isinstance(boek_data['auteur'], str) and not boek_data['auteur'].strip())
        ):
            raise OngeldigeBoekDataException()
        cursor = self.db_connection.cursor()
        try:
            query = "UPDATE boeken SET titel=?, auteur=? WHERE id=?"
            cursor.execute(query, (boek_data['titel'], boek_data['auteur'], boek_id))
            if cursor.rowcount == 0:
                cursor.close()
                raise BoekNietGevondenException()
            self.db_connection.commit()
        finally:
            cursor.close()