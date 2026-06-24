class GebruikerReadException(Exception):
    """Base exception for GebruikerRead feature in GebruikerService."""
    pass

class GebruikerNotFoundException(GebruikerReadException):
    """Raised when a gebruiker (user) is not found."""
    pass

class GebruikerReadDatabaseException(GebruikerReadException):
    """Raised when a database error occurs while reading gebruiker."""
    pass

class InvalidGebruikerQueryException(GebruikerReadException):
    """Raised when the query parameters for gebruiker read are invalid."""
    pass

class UnauthorizedGebruikerReadException(GebruikerReadException):
    """Raised when the user is not authorized to read gebruiker info."""
    pass