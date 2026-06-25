from src.services.boekdeleteservice_exceptions import BoekNietGevondenException, BoekDatabaseFoutException

class BoekDeleteService:
    def __init__(self, repository):
        self.repository = repository

    def delete_boek(self, boek_id):
        if not self.repository.exists(boek_id):
            raise BoekNietGevondenException(f"Boek met id {boek_id} niet gevonden.")
        try:
            self.repository.delete(boek_id)
        except BoekDatabaseFoutException as ex:
            raise ex
