class BoekReadServiceException(Exception):
    """Base exception for BoekReadService errors."""
    pass

class BoekNotFoundException(BoekReadServiceException):
    """Raised when a requested Boek is not found in the database."""
    pass

class BoekReadDatabaseException(BoekReadServiceException):
    """Raised when a database error occurs while reading Boeken."""
    pass

# Alias for compatibility with tests
DatabaseReadException = BoekReadDatabaseException

class InvalidBoekQueryException(BoekReadServiceException):
    """Raised when an invalid query is used for reading Boeken."""
    pass

class MultipleBoekenNotFoundException(BoekReadServiceException):
    """Raised when multiple requested Boeken are not found."""
    pass
