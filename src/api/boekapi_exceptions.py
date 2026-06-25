class BoekAPIException(Exception):
    """Base exception for BoekAPI errors."""
    pass

class BoekNotFoundException(BoekAPIException):
    """Raised when a requested boek is not found."""
    pass

class BoekValidationException(BoekAPIException):
    """Raised when boek data is invalid."""
    pass

class BoekCreationException(BoekAPIException):
    pass

class BoekUpdateException(BoekAPIException):
    pass

class BoekDeletionException(BoekAPIException):
    pass

class BoekAPIUnauthorizedException(BoekAPIException):
    pass
