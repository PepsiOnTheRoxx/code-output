class BoekCreateException(Exception):
    """Base exception for BoekCreate feature in BoekService."""
    pass

class BoekCreateValidationException(BoekCreateException):
    """Raised when book data validation fails."""
    pass

class BoekCreateDatabaseException(BoekCreateException):
    """Raised when book creation fails due to database errors."""
    pass

class BoekCreateDuplicateException(BoekCreateException):
    """Raised when attempting to create a duplicate Boek record."""
    pass

class BoekCreatePermissionException(BoekCreateException):
    """Raised when user lacks permission to create Boek records."""
    pass