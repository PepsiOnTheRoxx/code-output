class BronDeleteException(Exception):
    """Base exception for BronDelete feature in BronService."""
    pass

class BronNotFoundException(BronDeleteException):
    """Exception raised when a Bron object to delete is not found."""
    pass

class BronDeletePermissionDenied(BronDeleteException):
    """Exception raised when deletion of a Bron is not permitted."""
    pass

class BronDeleteDependencyExists(BronDeleteException):
    """Exception raised when dependent objects prevent Bron deletion."""
    pass

class BronDeleteValidationError(BronDeleteException):
    """Exception raised when deletion input validation fails."""
    pass

class BronDeleteInternalError(BronDeleteException):
    """Exception raised for internal errors during Bron deletion."""
    pass