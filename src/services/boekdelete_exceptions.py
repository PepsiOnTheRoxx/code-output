class BoekDeleteException(Exception):
    """Base exception for BoekDelete feature in BoekService."""
    pass

class BoekNotFoundException(BoekDeleteException):
    """Raised when the specified Boek is not found."""
    pass

class BoekDeletePermissionException(BoekDeleteException):
    """Raised when user has no permission to delete the Boek."""
    pass

class BoekDeleteDependencyException(BoekDeleteException):
    """Raised when the Boek cannot be deleted due to dependencies."""
    pass

class BoekDeleteDatabaseException(BoekDeleteException):
    """Raised when a database error occurs during Boek deletion."""
    pass

class BoekDeleteValidationException(BoekDeleteException):
    """Raised when validation fails for Boek deletion."""
    pass