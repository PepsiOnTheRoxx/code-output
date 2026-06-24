class GebruikerUpdateException(Exception):
    """Base exception for GebruikerUpdate feature."""
    pass

class GebruikerNietGevondenException(GebruikerUpdateException):
    """Raised when a gebruiker is not found."""
    pass

class OngeldigeGebruikerDataException(GebruikerUpdateException):
    """Raised when provided gebruiker data is invalid."""
    pass

class GebruikerUpdateNietToegestaanException(GebruikerUpdateException):
    """Raised when gebruiker update is not allowed."""
    pass

class GebruikerUpdateMisluktException(GebruikerUpdateException):
    """Raised when an error occurs during gebruiker update process."""
    pass