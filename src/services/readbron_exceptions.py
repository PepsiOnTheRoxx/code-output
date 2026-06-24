class ReadBronException(Exception):
    """Base exception for ReadBron feature in BronService."""
    pass

class BronNotFoundException(ReadBronException):
    """Raised when the requested Bron cannot be found."""
    pass

class BronAccessDeniedException(ReadBronException):
    """Raised when access to the Bron is denied."""
    pass

class BronReadFailedException(ReadBronException):
    """Raised when reading the Bron fails due to a generic error."""
    pass