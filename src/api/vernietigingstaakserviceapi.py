from src.api.vernietigingstaakserviceapi_exceptions import (
    VernietigingstaakNotFoundException,
    VernietigingstaakValidationException,
    VernietigingstaakConflictException,
)

class VernietigingstaakService:
    @staticmethod
    def create(data):
        raise NotImplementedError

    @staticmethod
    def get(taak_id):
        raise NotImplementedError

    @staticmethod
    def update(taak_id, data):
        raise NotImplementedError

    @staticmethod
    def delete(taak_id):
        raise NotImplementedError

    @staticmethod
    def list():
        raise NotImplementedError

class VernietigingstaakAPI:
    def create_vernietigingstaak(self, vernietigingstaak_data):
        return VernietigingstaakService.create(vernietigingstaak_data)

    def get_vernietigingstaak(self, taak_id):
        return VernietigingstaakService.get(taak_id)

    def update_vernietigingstaak(self, taak_id, update_data):
        return VernietigingstaakService.update(taak_id, update_data)

    def delete_vernietigingstaak(self, taak_id):
        return VernietigingstaakService.delete(taak_id)

    def list_vernietigingstaken(self):
        return VernietigingstaakService.list()