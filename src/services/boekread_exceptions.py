class BoekReadException(Exception):
    """Base exception for BoekRead feature in BoekService."""
    pass

class BoekNotFoundException(BoekReadException):
    """Raised when a Boek cannot be found."""
    pass

class BoekServiceUnavailableException(BoekReadException):
    """Raised when the BoekService is unavailable."""
    pass

class BoekInvalidQueryException(BoekReadException):
    """Raised when the query for Boek is invalid."""
    pass

class BoekPermissionDeniedException(BoekReadException):
    """Raised when user does not have permission to read Boek."""
    pass

class BoekReadTimeoutException(BoekReadException):
    """Raised when reading a Boek takes too long."""
    pass