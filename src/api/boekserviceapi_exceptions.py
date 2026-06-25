class BoekAPIException(Exception):
    """Base exception for BoekAPI errors."""
    pass

class BoekAPINotFoundException(BoekAPIException):
    """Exception raised when a requested resource is not found."""
    pass

class BoekAPIValidationException(BoekAPIException):
    """Exception raised for input validation errors."""
    pass

class BoekAPIConflictException(BoekAPIException):
    """Exception raised for conflicts, e.g. duplicate entries."""
    pass

class BoekAPIUnauthorizedException(BoekAPIException):
    """Exception raised for unauthorized access."""
    pass

class BoekAPIInternalErrorException(BoekAPIException):
    """Exception raised for internal server errors."""
    pass