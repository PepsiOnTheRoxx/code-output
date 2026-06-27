class BoekReadException(Exception):
    """Base exception for BoekRead in BoekService."""
    pass

class BoekNotFoundException(BoekReadException):
    """Raised when the requested Boek is not found."""
    pass

class BoekReadPermissionException(BoekReadException):
    """Raised when there are insufficient permissions to read a Boek."""
    pass

class BoekReadInvalidInputException(BoekReadException):
    """Raised when input parameters for Boek read are invalid."""
    pass

class BoekReadServiceUnavailableException(BoekReadException):
    """Raised when the Boek read service is unavailable."""
    pass

# Add alias for test compatibility
InvalidBoekIdException = BoekReadInvalidInputException
