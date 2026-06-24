class BronDeleteException(Exception):
    """Base exception for BronDelete feature."""
    pass

class BronNotFoundException(BronDeleteException):
    """Raised when the specified Bron is not found."""
    pass

class BronDeletePermissionDenied(BronDeleteException):
    """Raised when the user is not allowed to delete the Bron."""
    pass

class BronDeleteInUseException(BronDeleteException):
    """Raised when the Bron cannot be deleted because it is in use."""
    pass

class BronDeleteInvalidStateException(BronDeleteException):
    """Raised when the Bron is not in a deletable state."""
    pass
