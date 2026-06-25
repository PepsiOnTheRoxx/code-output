class BoekCreateException(Exception):
    """Base exception for BoekCreate feature in BoekService."""
    pass

class BoekCreateValidationException(BoekCreateException):
    """Raised when book data validation fails."""
    pass

class BoekCreateDatabaseException(BoekCreateException):
    """Raised when book creation fails due to database errors."""
    pass

class BoekAlreadyExistsException(BoekCreateException):
    """Raised when a book with the given identifier already exists."""
    pass
