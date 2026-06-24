from src.services.brondelete_exceptions import BronNotFoundException

class BronService:
    def get_bron_by_id(self, bron_id):
        raise NotImplementedError

    def delete_bron_by_id(self, bron_id):
        raise NotImplementedError

    def delete_bron(self, bron_id):
        bron = self.get_bron_by_id(bron_id)
        if bron is None:
            raise BronNotFoundException()
        self.delete_bron_by_id(bron_id)