class BoekReadException(Exception):
    """Base exception for BoekRead feature in BoekService."""
    pass

class BoekNotFoundException(BoekReadException):
    """Raised when a Boek object could not be found in the database."""
    pass

class BoekDatabaseConnectionException(BoekReadException):
    """Raised when there is a database connection error."""
    pass

class BoekAttributeReadException(BoekReadException):
    """Raised when reading attributes of a Boek object fails."""
    pass

class BoekInvalidQueryException(BoekReadException):
    """Raised when the executed query is invalid."""
    pass
