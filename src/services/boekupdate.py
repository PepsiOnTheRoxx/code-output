from src.services.boekupdate_exceptions import (
    BoekNotFoundException,
    BoekUpdateException
)

class BoekService:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def update_boek(self, boek_id, update_data):
        if not update_data or not isinstance(update_data, dict):
            raise BoekUpdateException("Geen update data gegeven of data is ongeldig.")

        columns = ", ".join([f"{key}=?" for key in update_data.keys()])
        values = list(update_data.values())
        values.append(boek_id)

        query = f"UPDATE boek SET {columns} WHERE id=?"

        try:
            with self.db_connection.cursor() as cursor:
                cursor.execute(query, values)
                if cursor.rowcount == 0:
                    raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden.")
                self.db_connection.commit()
                return True
        except BoekNotFoundException:
            raise
        except Exception as e:
            self.db_connection.rollback()
            raise BoekUpdateException(f"Fout bij bijwerken boek: {str(e)}")