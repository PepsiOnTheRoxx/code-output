class BoekDeleteServiceException(Exception):
    """Base exception for BoekDeleteService errors."""
    pass

class BoekNietGevondenException(BoekDeleteServiceException):
    """Raised when the Boek to delete is not found."""
    pass

class BoekVerwijderMisluktException(BoekDeleteServiceException):
    """Raised when deleting the Boek failed."""
    pass

class BoekDatabaseFoutException(BoekDeleteServiceException):
    """Raised when a database error occurs during Boek deletion."""
    pass
