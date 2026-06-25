class BoekUpdateException(Exception):
    """Base exception for BoekUpdate feature in BoekService."""
    pass

class BoekNotFoundException(BoekUpdateException):
    """Exception raised when the specified Boek does not exist."""
    pass

class InvalidBoekDataException(BoekUpdateException):
    """Exception raised when the Boek data fails validation."""
    pass

class BoekUpdateDatabaseException(BoekUpdateException):
    """Exception raised when a database error occurs during Boek update."""
    pass

class BoekUpdateNietToegestaanException(BoekUpdateException):
    """Exception raised when updating the Boek is not permitted."""
    pass
