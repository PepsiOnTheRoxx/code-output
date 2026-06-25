class BoekReadException(Exception):
    """Base exception for BoekRead feature in BoekService."""
    pass

class BoekNotFoundException(BoekReadException):
    """Raised when a Boek record is not found in the database."""
    pass

class BoekReadPermissionException(BoekReadException):
    """Raised when there is a lack of permission to read Boek records."""
    pass

class BoekReadDatabaseException(BoekReadException):
    """Raised when a database error occurs during Boek reading."""
    pass

class BoekReadInvalidQueryException(BoekReadException):
    """Raised when the query for reading Boek records is invalid."""
    pass