class DeleteBronException(Exception):
    """Base exception for DeleteBron feature in BronService."""
    pass

class BronNotFoundException(DeleteBronException):
    """Raised when the specified Bron is not found."""
    pass

class BronDeletePermissionException(DeleteBronException):
    """Raised when the user does not have permission to delete the Bron."""
    pass

class BronDeleteConflictException(DeleteBronException):
    """Raised when the Bron cannot be deleted due to related data or conflict."""
    pass

class BronDeleteValidationException(DeleteBronException):
    """Raised when the Bron does not meet the validation criteria for deletion."""
    pass

class BronDeleteInternalErrorException(DeleteBronException):
    """Raised when an unexpected internal error occurs during deletion."""
    pass