class DeleteBronException(Exception):
    """Base exception for DeleteBron feature in BronService."""
    pass

class BronNotFoundException(DeleteBronException):
    """Raised when the specified Bron object is not found."""
    pass

class BronDeletePermissionDeniedException(DeleteBronException):
    """Raised when deletion is not permitted due to insufficient rights."""
    pass

class BronDeleteDependencyException(DeleteBronException):
    """Raised when Bron cannot be deleted due to existing dependencies."""
    pass

class BronDeleteValidationException(DeleteBronException):
    """Raised when validation fails before deleting Bron."""
    pass

class BronDeleteInternalException(DeleteBronException):
    """Raised when an unexpected internal error occurs during Bron deletion."""
    pass