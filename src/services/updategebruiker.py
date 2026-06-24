from src.services.updategebruiker_exceptions import GebruikerNietGevondenException, OnjuisteGebruikerDataException

# Dummy in-memory DB for illustrative purposes
_DUMMY_DB = {
    1: {"id": 1, "naam": "Oud", "email": "oud@domein.nl"},
    2: {"id": 2, "naam": "Test", "email": "test@domein.nl"},
    3: {"id": 3, "naam": "Tom", "email": "tom@domein.nl"},
}

class GebruikerRepository:
    def get_by_id(self, gebruiker_id):
        # Simuleer DB lookup
        return _DUMMY_DB.get(gebruiker_id, None)

    def update(self, gebruiker, nieuwe_data):
        if gebruiker is None:
            raise GebruikerNietGevondenException()
        # Simpele validatie: bijvoorbeeld email moet een "@" bevatten als die wordt aangepast
        if "email" in nieuwe_data and "@" not in nieuwe_data["email"]:
            raise OnjuisteGebruikerDataException("Ongeldig email-formaat")
        gebruiker_id = gebruiker["id"]
        _DUMMY_DB[gebruiker_id].update(nieuwe_data)
        return _DUMMY_DB[gebruiker_id]

def update_gebruiker(gebruiker_id, nieuwe_data):
    repository = GebruikerRepository()
    gebruiker = repository.get_by_id(gebruiker_id)
    if gebruiker is None:
        raise GebruikerNietGevondenException(f"Gebruiker met id {gebruiker_id} niet gevonden")
    try:
        result = repository.update(gebruiker, nieuwe_data)
        return result
    except OnjuisteGebruikerDataException as e:
        raise