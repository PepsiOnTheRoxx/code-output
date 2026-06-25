class BoekDeleteServiceException(Exception):
    """Base exception for BoekDeleteService errors."""
    pass

class BoekNietGevondenException(BoekDeleteServiceException):
    """Exception raised when a book is not found in the database."""
    pass

class BoekVerwijderFoutException(BoekDeleteServiceException):
    """Exception raised when there is an error deleting the book."""
    pass

class DatabaseVerbindingsFoutException(BoekDeleteServiceException):
    """Exception raised when there is a database connection error."""
    pass