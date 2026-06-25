class BoekUpdateException(Exception):
    """Base exception for BoekUpdate feature."""
    pass

class BoekNotFoundException(BoekUpdateException):
    """Exception raised when the specified boek does not exist in the database."""
    pass

class BoekUpdateValidationException(BoekUpdateException):
    """Exception raised for validation errors during boek update."""
    pass

class BoekDatabaseException(BoekUpdateException):
    """Exception raised for database errors during boek update."""
    pass

class BoekUpdatePermissionDeniedException(BoekUpdateException):
    """Exception raised when update operation is not permitted."""
    pass
