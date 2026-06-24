from src.api.gebruikerserviceapi_exceptions import (
    GebruikerNotFoundException,
    GebruikerAlreadyExistsException,
    GebruikerValidationException,
)

class GebruikerService:
    _db = {}  # Simulatie in-memory database
    _id_counter = 1

    def get_by_id(self, gebruiker_id):
        gebruiker = self._db.get(gebruiker_id)
        if gebruiker is None:
            raise GebruikerNotFoundException(f"Gebruiker met id {gebruiker_id} niet gevonden.")
        return gebruiker.copy()

    def create(self, gebruiker_data):
        # Basisvalidatie
        if not isinstance(gebruiker_data, dict):
            raise GebruikerValidationException("Gegevens moeten een dictionary zijn.")
        naam = gebruiker_data.get("naam")
        email = gebruiker_data.get("email")
        if not naam or not isinstance(email, str) or "@" not in email:
            raise GebruikerValidationException("Ongeldige naam of e-mail.")
        # Voorkom dubbele gebruiker (op email)
        for user in self._db.values():
            if user["email"].lower() == email.lower():
                raise GebruikerAlreadyExistsException(f"Gebruiker met email {email} bestaat al.")
        # Maak nieuwe gebruiker aan
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
        # Prevent email conflict
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
