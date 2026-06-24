class BronAPIException(Exception):
    """Base exception for BronAPI errors."""
    pass

class BronAPINotFoundException(BronAPIException):
    """Raised when the requested ObjectType is not found."""
    pass

class BronAPIValidationException(BronAPIException):
    """Raised when input data for ObjectType fails validation."""
    pass

class BronAPIUnauthorizedException(BronAPIException):
    """Raised when user is not authorized to perform an action on ObjectType."""
    pass

class BronAPIConflictException(BronAPIException):
    """Raised when a conflict occurs while processing ObjectType (e.g. duplicate entry)."""
    pass

class BronAPIInternalException(BronAPIException):
    """Raised for unexpected internal server errors in BronAPI related to ObjectType."""
    pass