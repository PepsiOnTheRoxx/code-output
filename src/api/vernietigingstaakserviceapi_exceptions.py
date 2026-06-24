class VernietigingstaakServiceAPIException(Exception):
    """Base exception for VernietigingstaakServiceAPI errors."""
    pass

class VernietigingstaakNotFoundError(VernietigingstaakServiceAPIException):
    """Raised when a Vernietigingstaak is not found."""
    pass

class VernietigingstaakValidationError(VernietigingstaakServiceAPIException):
    """Raised when provided data for Vernietigingstaak is invalid."""
    pass

class VernietigingstaakPermissionDenied(VernietigingstaakServiceAPIException):
    """Raised when permission is denied for an operation."""
    pass

class VernietigingstaakConflictError(VernietigingstaakServiceAPIException):
    """Raised when a conflict occurs, e.g., duplicate Vernietigingstaak."""
    pass

class VernietigingstaakServiceUnavailable(VernietigingstaakServiceAPIException):
    """Raised when the Vernietigingstaak service is unavailable."""
    pass