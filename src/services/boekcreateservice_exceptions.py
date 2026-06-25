class BoekCreateServiceException(Exception):
    """Base exception for errors in BoekCreateService."""
    pass

class BoekAlreadyExistsException(BoekCreateServiceException):
    """Raised when a boek with the given identifier already exists."""
    pass

class InvalidBoekDataException(BoekCreateServiceException):
    """Raised when provided boek data is invalid."""
    pass

class BoekDatabaseException(BoekCreateServiceException):
    """Raised when there is a database error during boek creation."""
    pass

class BoekServiceDependencyException(BoekCreateServiceException):
    """Raised when a dependency service fails during boek creation."""
    pass