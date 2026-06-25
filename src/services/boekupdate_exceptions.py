class BoekUpdateException(Exception):
    """Base exception for BoekUpdate feature in BoekService."""
    pass

class BoekNotFoundException(BoekUpdateException):
    """Exception raised when a boek is not found during update."""
    pass

class BoekUpdateValidationException(BoekUpdateException):
    """Exception raised when data validation fails during boek update."""
    pass

class BoekUpdatePermissionException(BoekUpdateException):
    """Exception raised when the user has insufficient permissions to update a boek."""
    pass

class BoekUpdateConflictException(BoekUpdateException):
    """Exception raised when there is a conflict while updating a boek (e.g. concurrent update)."""
    pass

class BoekUpdateDatabaseException(BoekUpdateException):
    """Exception raised when a database error occurs during boek update."""
    pass

