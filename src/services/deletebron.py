from src.services.deletebron_exceptions import BronNotFoundException, DeleteBronException

class BronService:
    def __init__(self):
        # Simuleer een eenvoudige interne opslag
        self._brons = {}
    
    def add_bron(self, bron):
        self._brons[bron.id] = bron

    def get_bron_by_id(self, bron_id):
        # Return the bron if exists, otherwise None
        return self._brons.get(bron_id, None)

    def delete_bron(self, bron_id):
        if bron_id not in self._brons:
            raise BronNotFoundException(f"Bron with id {bron_id} not found")
        del self._brons[bron_id]
        return None

class DeleteBron:
    def __init__(self, bron_service):
        self.bron_service = bron_service

    def execute(self, bron_id):
        bron = self.bron_service.get_bron_by_id(bron_id)
        if bron is None:
            raise BronNotFoundException(f"Bron with id {bron_id} not found")
        try:
            self.bron_service.delete_bron(bron_id)
        except DeleteBronException as e:
            raise e
