class GebruikerServiceException(Exception):
    """Basisklasse voor GebruikerService gerelateerde exceptions."""
    pass

class GebruikerAanmakenException(GebruikerServiceException):
    """Fout opgetreden tijdens het aanmaken van een gebruiker."""
    pass

class OngeldigeGebruikerNaamException(GebruikerAanmakenException):
    """De opgegeven gebruikersnaam is ongeldig."""
    pass

class OngeldigEmailadresException(GebruikerAanmakenException):
    """Het opgegeven emailadres is ongeldig."""
    pass

class GebruikerBestaatAlException(GebruikerAanmakenException):
    """Er bestaat al een gebruiker met deze naam of emailadres."""
    pass