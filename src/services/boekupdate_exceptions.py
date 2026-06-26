class BoekUpdateException(Exception):
    """Base exception for Boek update feature in BoekService."""
    pass

class BoekNotFoundException(BoekUpdateException):
    """Raised when the Boek object to update is not found."""
    pass

class InvalidBoekDataException(BoekUpdateException):
    """Raised when provided data for updating Boek is invalid."""
    pass

class BoekUpdateConflictException(BoekUpdateException):
    """Raised when there is a conflict during updating Boek (e.g., concurrent update)."""
    pass

class BoekUpdatePermissionException(BoekUpdateException):
    """Raised when the user lacks permission to update Boek."""
    pass

class BoekUpdateDatabaseException(BoekUpdateException):
    """Raised when a database error occurs during Boek update."""
    pass
