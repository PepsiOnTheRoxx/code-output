class VernietigingstaakServiceAPIException(Exception):
    """Base exception for VernietigingstaakServiceAPI errors."""
    pass

class VernietigingstaakNotFoundException(VernietigingstaakServiceAPIException):
    """Raised when a Vernietigingstaak is not found."""
    pass

class VernietigingstaakValidationException(VernietigingstaakServiceAPIException):
    """Raised when provided data for Vernietigingstaak is invalid."""
    pass

class VernietigingstaakPermissionDenied(VernietigingstaakServiceAPIException):
    """Raised when permission is denied for an operation."""
    pass

class VernietigingstaakConflictException(VernietigingstaakServiceAPIException):
    """Raised when a conflict occurs, e.g., duplicate Vernietigingstaak."""
    pass

class VernietigingstaakServiceUnavailable(VernietigingstaakServiceAPIException):
    """Raised when the Vernietigingstaak service is unavailable."""
    pass
