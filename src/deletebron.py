from src.deletebron_exceptions import *

class BronService:
    def __init__(self, bron_repo):
        self.bron_repo = bron_repo

    def delete_bron(self, bron_id):
        bron = self.bron_repo.get_by_id(bron_id)
        if bron is None:
            raise BronNotFoundException()
        if self.bron_repo.is_in_use(bron_id):
            raise BronInUseException()
        self.bron_repo.delete(bron_id)