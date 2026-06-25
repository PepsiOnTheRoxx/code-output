class BoekReadException(Exception):
    """Base exception for BoekRead feature in BoekService."""
    pass

class BoekNotFoundException(BoekReadException):
    """Raised when the requested book does not exist in the database."""
    pass

class BoekDatabaseReadException(BoekReadException):
    """Raised when there is a database error during book read operation."""
    pass

class BoekInvalidQueryException(BoekReadException):
    """Raised when the query for reading a book is invalid."""
    pass