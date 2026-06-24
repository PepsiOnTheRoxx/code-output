class GebruikerNotFoundException(Exception):
    pass

class InvalidGebruikerDataException(Exception):
    pass

class UserService:
    def __init__(self):
        self._gebruikers = {}

    def update_gebruiker(self, gebruiker_id, updated_data):
        if not isinstance(gebruiker_id, int) or gebruiker_id not in self._gebruikers:
            raise GebruikerNotFoundException()

        if updated_data is None:
            raise InvalidGebruikerDataException()

        if not isinstance(updated_data, dict):
            raise InvalidGebruikerDataException()

        gebruiker = self._gebruikers[gebruiker_id]
        nieuwe_naam = gebruiker['naam']
        nieuwe_email = gebruiker['email']

        if 'naam' in updated_data:
            waarde = updated_data['naam']
            if waarde is not None:
                nieuwe_naam = waarde
        if 'email' in updated_data:
            waarde = updated_data['email']
            if waarde is not None:
                nieuwe_email = waarde

        if 'naam' in updated_data or 'email' in updated_data:
            self._gebruikers[gebruiker_id]['naam'] = nieuwe_naam
            self._gebruikers[gebruiker_id]['email'] = nieuwe_email

        # update only known fields, ignore extra
        # if nothing updated, just return original

        return dict(self._gebruikers[gebruiker_id])