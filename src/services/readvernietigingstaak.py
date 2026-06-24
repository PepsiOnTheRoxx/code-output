from src.services.readvernietigingstaak_exceptions import VernietigingstaakNotFound, InvalidVernietigingstaakID

class VernietigingstaakService:
    def read_vernietigingstaak(self, taak_id):
        return self.get_by_id(taak_id)

    def get_by_id(self, taak_id):
        raise NotImplementedError("Deze methode dient door een subclass of in de implementatie ingevuld te worden.")