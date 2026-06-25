class BoekAPIException(Exception):
    """Base exception for BoekAPI errors."""
    pass

class BoekNietGevondenException(BoekAPIException):
    """Raised when a requested book is not found."""
    pass

class BoekAlreadyExistsException(BoekAPIException):
    """Raised when attempting to create a book that already exists."""
    pass

class OngeldigeBoekDataException(BoekAPIException):
    """Raised when provided book data is invalid."""
    pass

class BoekCreationException(BoekAPIException):
    """Raised when an error occurs during book creation."""
    pass

class BoekUpdateException(BoekAPIException):
    """Raised when an error occurs during book update."""
    pass

class BoekDeletionException(BoekAPIException):
    """Raised when an error occurs during book deletion."""
    pass

class BoekAPIUnauthorizedException(BoekAPIException):
    """Raised when a user is not authorized to perform an operation."""
    pass

class BoekAPIDatabaseException(BoekAPIException):
    """Raised when a database error occurs in the BoekAPI."""
    pass
