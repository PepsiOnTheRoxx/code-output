class BoekReadException(Exception):
    """Base exception for BoekRead feature in BoekService."""
    pass

class BoekNotFoundException(BoekReadException):
    """Raised when a requested Boek is not found."""
    pass

class BoekReadPermissionException(BoekReadException):
    """Raised when lacking permission to read a Boek."""
    pass

class BoekReadInvalidInputException(BoekReadException):
    """Raised when given invalid input for reading Boek(en)."""
    pass

class BoekReadServiceUnavailableException(BoekReadException):
    """Raised when the BoekService is unavailable during read."""
    pass