from src.api.gebruikerserviceapi_exceptions import (
    GebruikerNotFoundException,
    GebruikerAlreadyExistsException,
    GebruikerValidationException,
)

# Houd de service singleton in deze module
class GebruikerService:
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._db = {}
            self._id_counter = 1
            self._initialized = True

    def get_by_id(self, gebruiker_id):
        gebruiker = self._db.get(gebruiker_id)
        if gebruiker is None:
            raise GebruikerNotFoundException(f"Gebruiker met id {gebruiker_id} niet gevonden.")
        return gebruiker.copy()

    def create(self, gebruiker_data):
        if not isinstance(gebruiker_data, dict):
            raise GebruikerValidationException("Gegevens moeten een dictionary zijn.")
        naam = gebruiker_data.get("naam")
        email = gebruiker_data.get("email")
        if not naam or not isinstance(email, str) or "@" not in email:
            raise GebruikerValidationException("Ongeldige naam of e-mail.")
        for user in self._db.values():
            if user["email"].lower() == email.lower():
                raise GebruikerAlreadyExistsException(f"Gebruiker met email {email} bestaat al.")
        gebruiker_id = self._id_counter
        self._id_counter += 1
        gebruiker = {
            "id": gebruiker_id,
            "naam": naam,
            "email": email,
        }
        self._db[gebruiker_id] = gebruiker
        return gebruiker.copy()

    def update(self, gebruiker_id, gebruiker_data):
        gebruiker = self._db.get(gebruiker_id)
        if gebruiker is None:
            raise GebruikerNotFoundException(f"Gebruiker met id {gebruiker_id} niet gevonden.")
        if not isinstance(gebruiker_data, dict):
            raise GebruikerValidationException("Gegevens moeten een dictionary zijn.")
        if "email" in gebruiker_data:
            email = gebruiker_data["email"]
            if not isinstance(email, str) or "@" not in email:
                raise GebruikerValidationException("Ongeldig e-mailadres.")
            for uid, user in self._db.items():
                if uid != gebruiker_id and user["email"].lower() == email.lower():
                    raise GebruikerAlreadyExistsException(f"Gebruiker met email {email} bestaat al.")
            gebruiker["email"] = email
        if "naam" in gebruiker_data:
            naam = gebruiker_data["naam"]
            if not naam:
                raise GebruikerValidationException("Ongeldige naam.")
            gebruiker["naam"] = naam
        self._db[gebruiker_id] = gebruiker
        return gebruiker.copy()

    def delete(self, gebruiker_id):
        if gebruiker_id not in self._db:
            raise GebruikerNotFoundException(f"Gebruiker met id {gebruiker_id} niet gevonden.")
        del self._db[gebruiker_id]
        return True

# Singleton service instantie
global _gebruiker_service_instance
try:
    _gebruiker_service_instance
except NameError:
    _gebruiker_service_instance = GebruikerService()

def get_gebruiker(gebruiker_id):
    return _gebruiker_service_instance.get_by_id(gebruiker_id)

def create_gebruiker(gebruiker_data):
    return _gebruiker_service_instance.create(gebruiker_data)

def update_gebruiker(gebruiker_id, gebruiker_data):
    return _gebruiker_service_instance.update(gebruiker_id, gebruiker_data)

def delete_gebruiker(gebruiker_id):
    return _gebruiker_service_instance.delete(gebruiker_id)
