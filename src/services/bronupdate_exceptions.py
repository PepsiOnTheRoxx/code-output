class BronUpdateException(Exception):
    """Base exception for BronUpdate feature in BronService."""
    pass

class BronNietGevondenException(BronUpdateException):
    """Exception thrown when the requested Bron could not be found."""
    pass

class OngeldigeBronDataException(BronUpdateException):
    """Exception thrown when provided data for the Bron is invalid."""
    pass

class BronUpdateNietToegestaanException(BronUpdateException):
    """Exception thrown when updating the Bron is not allowed."""
    pass

class BronUpdateFoutException(BronUpdateException):
    """Exception thrown when a general error occurs during Bron update."""
    pass