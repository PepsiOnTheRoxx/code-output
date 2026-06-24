class GebruikerUpdateException(Exception):
    """Base exception for GebruikerUpdate feature."""
    pass

class GebruikerNietGevondenException(GebruikerUpdateException):
    """Raised when a gebruiker is not found."""
    pass

class OngeldigeGebruikerUpdateException(GebruikerUpdateException):
    """Raised when provided gebruiker update data is invalid."""
    pass

class GebruikerUpdateNietToegestaanException(GebruikerUpdateException):
    """Raised when gebruiker update is not allowed."""
    pass

class GebruikerUpdateMisluktException(GebruikerUpdateException):
    """Raised when an error occurs during gebruiker update process."""
    pass

class DatabaseFoutException(Exception):
    pass
