class BoekUpdateException(Exception):
    """Base exception for BoekUpdate feature in BoekService."""
    pass

class BoekNotFoundException(BoekUpdateException):
    """Raised when a book to update is not found."""
    pass

class InvalidBoekDataException(BoekUpdateException):
    """Raised when provided book data is invalid for update."""
    pass

class BoekUpdatePermissionException(BoekUpdateException):
    """Raised when the user does not have permission to update the book."""
    pass

class BoekUpdateConflictException(BoekUpdateException):
    """Raised when there is a conflict during the book update."""
    pass

class BoekUpdateDatabaseException(BoekUpdateException):
    """Raised when a database error occurs during book update."""
    pass