class BoekReadException(Exception):
    """Base exception for BoekRead feature in BoekService."""
    pass

class BoekNietGevondenException(BoekReadException):
    """Raised when a requested boek cannot be found."""
    pass

class BoekReadValidationException(BoekReadException):
    """Raised when the read request for boek contains invalid data."""
    pass

class BoekReadUnauthorizedException(BoekReadException):
    """Raised when the user is not authorized to read boek data."""
    pass

class DatabaseFoutException(BoekReadException):
    """Raised when a database error occurs during boek read."""
    pass
