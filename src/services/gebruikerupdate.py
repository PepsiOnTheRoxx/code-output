from src.services.gebruikerupdate_exceptions import (
    GebruikerNietGevondenException,
    OngeldigeGebruikerDataException,
)

class GebruikerService:
    def vind_gebruiker_op_id(self, gebruiker_id):
        raise NotImplementedError

    def opslaan_gebruiker(self, gebruiker_dict):
        raise NotImplementedError

    def update_gebruiker(self, payload):
        if not isinstance(payload, dict) or "id" not in payload:
            raise OngeldigeGebruikerDataException("ID is verplicht")
        gebruiker_id = payload["id"]
        gebruiker = self.vind_gebruiker_op_id(gebruiker_id)
        if gebruiker is None:
            raise GebruikerNietGevondenException(f"Gebruiker met id {gebruiker_id} bestaat niet")

        nieuwe_naam = payload.get("naam", gebruiker.get("naam"))
        if not isinstance(nieuwe_naam, str) or not nieuwe_naam.strip():
            raise OngeldigeGebruikerDataException("Naam is ongeldig of leeg")

        nieuwe_email = payload.get("email", gebruiker.get("email"))
        if "email" in payload:
            if not isinstance(nieuwe_email, str) or "@" not in nieuwe_email or not nieuwe_email.strip():
                raise OngeldigeGebruikerDataException("Email is ongeldig")

        else:
            nieuwe_email = gebruiker.get("email")

        updated_gebruiker = dict(gebruiker)
        updated_gebruiker["naam"] = nieuwe_naam
        updated_gebruiker["email"] = nieuwe_email

        self.opslaan_gebruiker(updated_gebruiker)