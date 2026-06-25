class BoekAPIException(Exception):
    """Base exception for BoekAPI."""
    pass

class BoekAPINotFoundException(BoekAPIException):
    """Exception raised when a requested book is not found."""
    pass

class BoekAPIValidationException(BoekAPIException):
    """Exception raised when input validation fails."""
    pass

class BoekAPIDatabaseException(BoekAPIException):
    """Exception raised on database errors."""
    pass

class BoekAPIUnauthorizedException(BoekAPIException):
    """Exception raised when authentication fails."""
    pass

class BoekAPIConflictException(BoekAPIException):
    """Exception raised when a resource conflict occurs."""
    pass
