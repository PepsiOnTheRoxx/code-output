class BronReadException(Exception):
    """Raised when reading the Bron fails due to a generic error."""
    pass

class BronNotFoundException(BronReadException):
    """Raised when the requested Bron cannot be found."""
    pass

class BronAccessDeniedException(BronReadException):
    """Raised when access to the Bron is denied."""
    pass
