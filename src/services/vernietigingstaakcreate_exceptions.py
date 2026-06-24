class VernietigingstaakAlreadyExistsException(Exception):
    """Raised when a Vernietigingstaak already exists."""
    pass

class InvalidVernietigingstaakDataException(Exception):
    """Raised when the input data for Vernietigingstaak is invalid or incomplete."""
    pass

class DatabaseException(Exception):
    """Generic database or persistence exception."""
    pass
