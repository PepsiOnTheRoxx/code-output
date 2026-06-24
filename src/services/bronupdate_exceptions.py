class BronUpdateException(Exception):
    """Base exception for BronUpdate feature in BronService."""
    pass

class BronUpdateNotFoundException(BronUpdateException):
    """Raised when the specified Bron to update is not found."""
    pass

class BronUpdateValidationException(BronUpdateException):
    """Raised when provided data for updating Bron is invalid."""
    pass

class BronUpdatePermissionException(BronUpdateException):
    """Raised when user does not have permission to update Bron."""
    pass

class BronUpdateDatabaseException(BronUpdateException):
    """Raised when a database error occurs during Bron update."""
    pass