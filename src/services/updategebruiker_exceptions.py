class UpdateGebruikerException(Exception):
    """Base exception for UpdateGebruiker feature in GebruikerService."""
    pass

class GebruikerNietGevondenException(UpdateGebruikerException):
    """Exception for when the specified gebruiker is not found."""
    pass

class OnjuisteGebruikerDataException(UpdateGebruikerException):
    """Exception for when the gebruiker data provided is incorrect or invalid."""
    pass

class GebruikerUpdateMisluktException(UpdateGebruikerException):
    """Exception for when updating the gebruiker fails."""
    pass

class NietGeautoriseerdVoorUpdateException(UpdateGebruikerException):
    """Exception for unauthorized update attempts."""
    pass
