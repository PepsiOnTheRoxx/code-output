from src.services.updategebruiker_exceptions import GebruikerNietGevonden, OngeldigeGebruikerData

class GebruikerRepository:
    def get_by_id(self, gebruiker_id):
        raise NotImplementedError

    def update(self, gebruiker, nieuwe_data):
        raise NotImplementedError

def update_gebruiker(gebruiker_id, nieuwe_data):
    repository = GebruikerRepository()
    gebruiker = repository.get_by_id(gebruiker_id)
    if gebruiker is None:
        raise GebruikerNietGevonden(f"Gebruiker met id {gebruiker_id} niet gevonden")

    try:
        result = repository.update(gebruiker, nieuwe_data)
        return result
    except OngeldigeGebruikerData as e:
        raise