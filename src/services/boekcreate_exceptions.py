class BoekCreateException(Exception):
    """Base exception for BoekCreate feature in BoekService."""
    pass

class BoekCreateDatabaseException(BoekCreateException):
    """Raised when an error occurs during the SQLite database operation."""
    pass

class BoekCreateMissingAttributeException(BoekCreateException):
    """Raised when a required attribute is missing for Boek creation."""
    pass

class BoekCreateInvalidAttributeException(BoekCreateException):
    """Raised when an attribute value is invalid for Boek creation."""
    pass

class BoekCreateDuplicateException(BoekCreateException):
    """Raised when trying to create a Boek that already exists."""
    pass