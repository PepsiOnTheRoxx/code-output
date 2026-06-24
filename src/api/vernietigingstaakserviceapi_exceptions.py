class VernietigingstaakAPIException(Exception):
    """Base exception for VernietigingstaakAPI related errors."""
    pass

class VernietigingstaakAPINotFoundException(VernietigingstaakAPIException):
    """Exception raised when a requested Vernietigingstaak resource is not found."""
    pass

class VernietigingstaakAPIValidationException(VernietigingstaakAPIException):
    """Exception raised when input validation fails for Vernietigingstaak API."""
    pass

class VernietigingstaakAPIUnauthorizedException(VernietigingstaakAPIException):
    """Exception raised when authentication or authorization fails."""
    pass

class VernietigingstaakAPIConflictException(VernietigingstaakAPIException):
    """Exception raised when there is a conflict in the Vernietigingstaak API (e.g., duplicate entry)."""
    pass

class VernietigingstaakAPIInternalException(VernietigingstaakAPIException):
    """Exception for unexpected internal errors in Vernietigingstaak API."""
    pass