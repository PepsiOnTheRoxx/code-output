class BoekUpdateException(Exception):
    """Base exception for BoekUpdate feature."""
    pass

class BoekNietGevondenException(BoekUpdateException):
    """Exception raised when a Boek is not found."""
    pass

class BoekUpdateValidatieException(BoekUpdateException):
    """Exception raised when validation fails during Boek update."""
    pass

class BoekUpdatePermissieException(BoekUpdateException):
    """Exception raised when update is not permitted for Boek."""
    pass

class BoekUpdateDatabaseException(BoekUpdateException):
    """Exception raised when a database error occurs during Boek update."""
    pass
