class BronAPIException(Exception):
    """Base exception for BronAPI related errors."""
    pass

class BronAPINotFoundException(BronAPIException):
    """Exception raised when a requested resource is not found."""
    pass

class BronAPIInvalidRequestException(BronAPIException):
    """Exception raised for invalid API requests."""
    pass

class BronAPIUnauthorizedException(BronAPIException):
    """Exception raised for unauthorized API access."""
    pass

class BronAPIInternalErrorException(BronAPIException):
    """Exception raised for internal errors in the BronAPI component."""
    pass