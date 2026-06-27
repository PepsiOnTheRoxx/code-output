class BoekReadException(Exception):
    """Base exception for BoekRead feature errors."""
    pass

class BoekReadNotFoundException(BoekReadException):
    """Exception raised when a Boek is not found."""
    pass

class BoekReadPermissionException(BoekReadException):
    """Exception raised when user lacks permission to read a Boek."""
    pass

class BoekReadInvalidRequestException(BoekReadException):
    """Exception raised when a request for Boek read is invalid."""
    pass

class BoekReadServiceUnavailableException(BoekReadException):
    """Exception raised when the Boek read service is unavailable."""
    pass
