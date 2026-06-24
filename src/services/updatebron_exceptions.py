class UpdateBronException(Exception):
    """Base exception for UpdateBron feature in BronService."""
    pass

class BronNotFoundException(UpdateBronException):
    """Raised when the specified Bron does not exist."""
    pass

class InvalidBronDataException(UpdateBronException):
    """Raised when provided Bron data is invalid."""
    pass

class BronUpdateConflictException(UpdateBronException):
    """Raised when there is a version/conflict error during Bron update."""
    pass

class BronUpdatePermissionException(UpdateBronException):
    """Raised when user is not allowed to update the Bron."""
    pass

class BronUpdateUnknownException(UpdateBronException):
    """Raised when an unknown error occurs during Bron update."""
    pass