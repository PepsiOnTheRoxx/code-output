class ReadBronException(Exception):
    """Base exception for ReadBron feature in BronService."""
    pass

class ReadBronDataNotFoundException(ReadBronException):
    """Raised when requested Bron data is not found."""
    pass

class ReadBronInvalidElementTypeException(ReadBronException):
    """Raised when an invalid ElementType is encountered."""
    pass

class ReadBronInvalidElementIDException(ReadBronException):
    """Raised when an invalid ElementID is provided."""
    pass

class ReadBronDataAccessException(ReadBronException):
    """Raised when there is an issue accessing Bron data."""
    pass

# Export exceptions to be used directly from this file.
class BronNotFoundException(ReadBronDataNotFoundException):
    pass

class InvalidBronIDException(ReadBronInvalidElementIDException):
    pass
