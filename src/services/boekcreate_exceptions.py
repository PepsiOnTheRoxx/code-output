class BoekCreateException(Exception):
    """Baseline exception for BoekCreate feature in BoekService."""
    pass

class BoekValidationException(BoekCreateException):
    """Raised when Boek object validation fails."""
    pass

class BoekDatabaseException(BoekCreateException):
    """Raised when there is an SQLite database error during Boek creation."""
    pass

class BoekAlreadyExistsException(BoekCreateException):
    """Raised when trying to create a Boek that already exists."""
    pass

class BoekInvalidAttributeException(BoekValidationException):
    """Raised when a Boek attribute is invalid (e.g. None)."""
    pass

class BoekMissingAttributeException(BoekValidationException):
    """Raised when a required Boek attribute is missing."""
    pass

class BoekPersistenceException(BoekCreateException):
    """Raised when persisting Boek to the database fails."""
    pass

