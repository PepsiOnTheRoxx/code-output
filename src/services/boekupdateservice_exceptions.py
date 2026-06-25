class BoekUpdateServiceException(Exception):
    """Base exception for BoekUpdateService errors."""
    pass

class BoekNietGevondenException(BoekUpdateServiceException):
    """Raised when the specified book does not exist."""
    pass

class OngeldigeBoekDataException(BoekUpdateServiceException):
    """Raised when provided book data is invalid."""
    pass

class DatabaseUpdateException(BoekUpdateServiceException):
    """Raised when a database error occurs during book update."""
    pass

class UnauthorizedBoekUpdateException(BoekUpdateServiceException):
    """Raised when user is not authorized to update the book."""
    pass
