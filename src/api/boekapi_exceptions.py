class BoekAPIException(Exception):
    """Base exception for BoekAPI component."""
    pass

class BoekAPINotFoundException(BoekAPIException):
    """Exception raised when a requested Boek is not found."""
    pass

class BoekAPIValidationException(BoekAPIException):
    """Exception raised when input validation fails for Boek."""
    pass

class BoekAPIDatabaseException(BoekAPIException):
    """Exception raised for database errors in BoekAPI."""
    pass

class BoekAPIUnauthorizedException(BoekAPIException):
    """Exception raised when user is not authorized to perform an action on Boek."""
    pass

class BoekAPIConflictException(BoekAPIException):
    """Exception raised when a Boek already exists or conflict occurs."""
    pass
