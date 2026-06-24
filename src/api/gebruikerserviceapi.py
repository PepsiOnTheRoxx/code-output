from src.api.gebruikerserviceapi_exceptions import (
    GebruikerNotFoundException,
    GebruikerAlreadyExistsException,
    GebruikerValidationException,
)

class GebruikerService:
    def get_by_id(self, gebruiker_id):
        raise NotImplementedError()

    def create(self, gebruiker_data):
        raise NotImplementedError()

    def update(self, gebruiker_id, gebruiker_data):
        raise NotImplementedError()

    def delete(self, gebruiker_id):
        raise NotImplementedError()

def get_gebruiker(gebruiker_id):
    service = GebruikerService()
    return service.get_by_id(gebruiker_id)

def create_gebruiker(gebruiker_data):
    service = GebruikerService()
    return service.create(gebruiker_data)

def update_gebruiker(gebruiker_id, gebruiker_data):
    service = GebruikerService()
    return service.update(gebruiker_id, gebruiker_data)

def delete_gebruiker(gebruiker_id):
    service = GebruikerService()
    return service.delete(gebruiker_id)