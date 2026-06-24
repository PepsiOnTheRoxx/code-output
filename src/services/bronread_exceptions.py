class BronReadError(Exception):
    """Base exception for BronRead feature in BronService."""
    pass

class BronNotFoundError(BronReadError):
    """Raised when the requested Bron is not found."""
    pass

class BronReadPermissionError(BronReadError):
    """Raised when reading a Bron is not permitted."""
    pass

class BronReadConnectionError(BronReadError):
    """Raised when there is a connection issue during Bron retrieval."""
    pass

class BronReadInvalidRequestError(BronReadError):
    """Raised when the Bron read request is invalid."""
    pass

class BronReadMetamodelError(BronReadError):
    """Raised when Bron read encounters metamodel issues."""
    pass