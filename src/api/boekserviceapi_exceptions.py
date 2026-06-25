class BoekAPIException(Exception):
    """Base exception for BoekAPI."""
    pass

class BoekAPINotFoundException(BoekAPIException):
    """Exception raised when a requested boek is not found."""
    pass

class BoekAPIValidationException(BoekAPIException):
    """Exception raised for validation errors in BoekAPI."""
    pass

class BoekAPIConflictException(BoekAPIException):
    """Exception raised when there is a conflict in BoekAPI (e.g. duplicate boek)."""
    pass

class BoekAPIUnauthorizedException(BoekAPIException):
    """Exception raised for unauthorized access to BoekAPI."""
    pass

class BoekAPIInternalException(BoekAPIException):
    """Exception raised for internal errors in BoekAPI."""
    pass