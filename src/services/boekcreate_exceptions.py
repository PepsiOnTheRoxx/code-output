class BoekCreateException(Exception):
    """Base exception for BoekCreate errors."""
    pass

class BoekCreateDatabaseException(BoekCreateException):
    """Exception raised when a database error occurs during boek creation."""
    pass

class BoekCreateValidationException(BoekCreateException):
    """Exception raised when boek data is invalid."""
    pass

class BoekCreateUniqueConstraintException(BoekCreateException):
    """Exception raised when trying to create a boek that already exists (unique constraint violation)."""
    pass

class BoekCreateMissingAttributeException(BoekCreateException):
    """Exception raised when a required attribute is missing during boek creation."""
    pass

class BoekCreateInternalException(BoekCreateException):
    """Exception raised for any other internal errors during boek creation."""
    pass