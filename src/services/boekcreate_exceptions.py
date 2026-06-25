class BoekCreateException(Exception):
    """Base exception for boek_service.BookCreate feature."""
    pass

class BoekCreateDatabaseException(BoekCreateException):
    """Raised when a database error occurs during book creation."""
    pass

class BoekCreateValidationException(BoekCreateException):
    """Raised when validation of book attributes fails."""
    pass

class BoekCreateDuplicateException(BoekCreateException):
    """Raised when attempting to create a duplicate book."""
    pass

class BoekCreateMissingAttributeException(BoekCreateValidationException):
    """Raised when a required attribute is missing in book creation data."""
    pass

class BoekCreateInvalidAttributeException(BoekCreateValidationException):
    """Raised when an attribute value is invalid in book creation data."""
    pass