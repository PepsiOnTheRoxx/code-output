class GebruikerAPIException(Exception):
    """Base exception for GebruikerAPI errors."""
    pass

class GebruikerNotFoundException(GebruikerAPIException):
    """Gebruiker niet gevonden."""
    pass

class GebruikerAlreadyExistsException(GebruikerAPIException):
    """Aanmaken van gebruiker mislukt omdat deze al bestaat."""
    pass

class GebruikerValidationException(GebruikerAPIException):
    """De meegegeven gebruiker data is ongeldig."""
    pass

class GebruikerAPIAuthorisatieException(GebruikerAPIException):
    """Geen toestemming voor deze operatie."""
    pass
