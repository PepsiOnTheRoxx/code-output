class BoekUpdateException(Exception):
    """Base exception for BoekUpdate feature."""
    pass

class BoekNietGevondenException(BoekUpdateException):
    """Raised when the book to update is not found."""
    pass

class OngeldigeBoekDataException(BoekUpdateException):
    """Raised when provided book data is invalid."""
    pass

class BoekUpdateDatabaseException(BoekUpdateException):
    """Raised when a database error occurs during boek update."""
    pass

class BoekOngewijzigdException(BoekUpdateException):
    """Raised when no changes are made in the boek update process."""
    pass