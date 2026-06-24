class BronReadException(Exception):
    """Base exception for BronRead feature."""
    pass

class BronNotFoundException(BronReadException):
    """Raised when the requested Bron is not found."""
    pass

class BronServiceUnavailableException(BronReadException):
    """Raised when the BronService is unavailable."""
    pass

class InvalidBronIDException(BronReadException):
    """Raised when the provided Bron ID is invalid."""
    pass

class BronReadPermissionDeniedException(BronReadException):
    """Raised when the user does not have permission to read the Bron."""
    pass

class BronReadTimeoutException(BronReadException):
    """Raised when reading a Bron takes too long."""
    pass

class BronReadMetamodelMismatchException(BronReadException):
    """Raised when the Bron does not conform to the expected metamodel."""
    pass
