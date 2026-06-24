class VernietigingstaakReadError(Exception):
    """Base exception for VernietigingstaakRead errors."""
    pass

class VernietigingstaakNotFoundError(VernietigingstaakReadError):
    """Raised when a Vernietigingstaak could not be found."""
    pass

class VernietigingstaakPermissionDeniedError(VernietigingstaakReadError):
    """Raised when the user lacks permission to read the Vernietigingstaak."""
    pass

class VernietigingstaakInvalidRequestError(VernietigingstaakReadError):
    """Raised when the request for reading a Vernietigingstaak is invalid."""
    pass

class VernietigingstaakServiceUnavailableError(VernietigingstaakReadError):
    """Raised when the VernietigingstaakService is unavailable."""
    pass
