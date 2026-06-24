from src.services.deletebron_exceptions import BronNotFoundException, BronDeleteException

class BronService:
    def get_bron_by_id(self, bron_id):
        # Deze methode zou de bron ophalen.
        pass

    def delete_bron(self, bron_id):
        # Deze methode zou de bron verwijderen.
        pass

class DeleteBron:
    def __init__(self, bron_service):
        self.bron_service = bron_service

    def execute(self, bron_id):
        bron = self.bron_service.get_bron_by_id(bron_id)
        if bron is None:
            raise BronNotFoundException(f"Bron with id {bron_id} not found")
        self.bron_service.delete_bron(bron_id)