class BronCreateException(Exception):
    """Base exception for BronCreate feature."""
    pass

class BronCreateValidationException(BronCreateException):
    """Raised when validation fails during Bron creation."""
    pass

class BronCreateObjectTypeNotFoundException(BronCreateException):
    """Raised when the required ObjectType (ElementID: 12) is not found."""
    pass

class BronCreateAttribute15MissingException(BronCreateException):
    """Raised when attribute with ElementID 15 is missing."""
    pass

class BronCreateAttribute16MissingException(BronCreateException):
    """Raised when attribute with ElementID 16 is missing."""
    pass

class BronCreateDatabaseException(BronCreateException):
    """Raised when a database error occurs during Bron creation."""
    pass