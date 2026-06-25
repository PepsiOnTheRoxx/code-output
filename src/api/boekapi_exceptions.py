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
    """Raised when a boek cannot be created."""
    pass

class BoekUpdateException(BoekAPIException):
    """Raised when a boek cannot be updated."""
    pass

class BoekDeletionException(BoekAPIException):
    """Raised when a boek cannot be deleted."""
    pass

class BoekAPIUnauthorizedException(BoekAPIException):
    """Raised when an action is unauthorized."""
    pass