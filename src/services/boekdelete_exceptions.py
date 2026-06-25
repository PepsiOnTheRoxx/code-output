class BoekDeleteException(Exception):
    """Base exception for BoekDelete feature."""
    pass

class BoekNotFoundException(BoekDeleteException):
    """Raised when the requested boek is not found in the database."""
    pass

class BoekDeleteDatabaseException(BoekDeleteException):
    """Raised when a database error occurs during boek deletion."""
    pass

class BoekDeletePermissionDeniedException(BoekDeleteException):
    """Raised when the deletion is not permitted due to insufficient rights."""
    pass

class BoekDeleteInvalidIDException(BoekDeleteException):
    """Raised when an invalid ID is provided for deletion."""
    pass