from src.services.boekdeleteservice_exceptions import BoekNotFoundException, DatabaseException

class BoekDeleteService:
    def __init__(self, repository):
        self.repository = repository

    def delete_boek(self, boek_id):
        if not self.repository.exists(boek_id):
            raise BoekNotFoundException(f"Boek met id {boek_id} niet gevonden.")
        try:
            self.repository.delete(boek_id)
        except DatabaseException as ex:
            raise ex