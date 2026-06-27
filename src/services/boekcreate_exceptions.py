class BoekCreateException(Exception):
    """Base exception for BoekCreate feature in BoekService."""
    pass

class BoekCreateDataInvalidException(BoekCreateException):
    """Raised when the provided data for creating a Boek is invalid."""
    pass

class BoekCreateAlreadyExistsException(BoekCreateException):
    """Raised when a Boek to be created already exists."""
    pass

class BoekCreatePersistenceException(BoekCreateException):
    """Raised when there is a persistence/database error during Boek creation."""
    pass

class BoekCreateUnauthorizedException(BoekCreateException):
    """Raised when the creation of a Boek is not authorized."""
    pass

class BoekCreateUnknownException(BoekCreateException):
    """Raised when an unknown error occurs during Boek creation."""
    pass
