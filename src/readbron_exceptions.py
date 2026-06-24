class ReadBronException(Exception):
    """Base exception for ReadBron feature in BronService."""
    pass

class BronNotFoundException(ReadBronException):
    """Raised when the requested Bron is not found."""
    pass

class BronAccessDeniedException(ReadBronException):
    """Raised when access to the requested Bron is denied."""
    pass

class BronAttributeNotFoundException(ReadBronException):
    """Raised when a required Bron attribute (name or description) is missing."""
    pass

class BronInvalidObjectTypeException(ReadBronException):
    """Raised when the given ObjectType for Bron is invalid or not supported."""
    pass