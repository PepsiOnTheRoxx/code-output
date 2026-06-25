class BoekAPIException(Exception):
    """Base exception for BoekAPI feature."""
    pass

class BoekNotFoundException(BoekAPIException):
    """Raised when a requested Boek is not found."""
    pass

class BoekInvalidDataException(BoekAPIException):
    """Raised when provided Boek data is invalid."""
    pass

class BoekCreateException(BoekAPIException):
    """Raised when creation of a Boek fails."""
    pass

class BoekUpdateException(BoekAPIException):
    """Raised when updating a Boek fails."""
    pass

class BoekDeleteException(BoekAPIException):
    """Raised when deletion of a Boek fails."""
    pass

class BoekDatabaseException(BoekAPIException):
    """Raised when a general database error occurs in BoekAPI."""
    pass