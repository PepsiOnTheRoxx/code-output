class BoekDeleteException(Exception):
    """Base exception for BoekDelete feature in BoekService."""
    pass

class BoekNotFoundException(BoekDeleteException):
    """Raised when the specified Boek record is not found."""
    pass

class BoekDeletePermissionDenied(BoekDeleteException):
    """Raised when the user has no permission to delete the Boek."""
    pass

class BoekDeleteIntegrityError(BoekDeleteException):
    """Raised when the Boek cannot be deleted due to integrity constraints."""
    pass

class BoekDeleteValidationError(BoekDeleteException):
    """Raised when input validation fails during Boek delete operation."""
    pass