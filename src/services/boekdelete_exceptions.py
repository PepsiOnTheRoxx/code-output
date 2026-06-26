class BoekDeleteException(Exception):
    """Base exception for Boek delete functionality."""
    pass

class BoekNietGevondenException(BoekDeleteException):
    """Exception raised when the Boek to delete is not found."""
    pass

class BoekDeleteNietToegestaanException(BoekDeleteException):
    """Exception raised when deletion of Boek is not allowed."""
    pass

class BoekDeleteOnbekendeFoutException(BoekDeleteException):
    """Exception raised for unknown errors during Boek deletion."""
    pass