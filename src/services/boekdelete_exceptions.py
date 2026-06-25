class BoekDeleteException(Exception):
    """Base exception for BoekDelete feature."""
    pass

class BoekNietGevondenException(BoekDeleteException):
    """Exception raised when a book to be deleted is not found."""
    pass

class BoekDeleteDatabaseException(BoekDeleteException):
    """Exception raised for database errors during delete operation."""
    pass

class BoekDeleteOngeldigeInputException(BoekDeleteException):
    """Exception raised for invalid input for book delete."""
    pass