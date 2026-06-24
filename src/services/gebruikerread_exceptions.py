class GebruikerReadException(Exception):
    """Base exception for GebruikerRead errors."""
    pass

class GebruikerReadNotFoundException(GebruikerReadException):
    """Raised when a Gebruiker could not be found."""
    pass

class GebruikerReadInvalidInputException(GebruikerReadException):
    """Raised when the input for reading a Gebruiker is invalid."""
    pass

class GebruikerReadPermissionDeniedException(GebruikerReadException):
    """Raised when user does not have permissions to read a Gebruiker."""
    pass

class GebruikerReadInternalErrorException(GebruikerReadException):
    """Raised when an unexpected internal error occurs during Gebruiker read."""
    pass