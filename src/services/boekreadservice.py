from src.services.boekreadservice_exceptions import (
    BoekNotFoundException,
    DatabaseReadException,
)

class BoekReadService:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_boek_by_id(self, boek_id):
        try:
            boek = self.db_session.query().get(boek_id)
            if not boek:
                raise BoekNotFoundException(f"Boek with id {boek_id} not found.")
            return boek
        except BoekNotFoundException:
            raise
        except Exception as exc:
            raise DatabaseReadException(f"Database read error: {exc}")

    def get_all_boeken(self):
        try:
            boeken = self.db_session.query().all()
            return boeken
        except Exception as exc:
            raise DatabaseReadException(f"Database read error: {exc}")