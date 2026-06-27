class BoekAPIException(Exception):
    """Base exception for BoekAPI component."""
    pass

class BoekNotFoundException(BoekAPIException):
    """Raised when a Boek is not found."""
    pass

class BoekAlreadyExistsException(BoekAPIException):
    """Raised when trying to create a Boek that already exists (e.g. via ISBN)."""
    pass

class InvalidBoekDataException(BoekAPIException):
    """Raised when provided Boek data is invalid."""
    pass

class BoekCreateException(BoekAPIException):
    """Raised when there is an error creating a Boek."""
    pass

class BoekUpdateException(BoekAPIException):
    """Raised when there is an error updating a Boek."""
    pass

class BoekDeleteException(BoekAPIException):
    """Raised when there is an error deleting a Boek."""
    pass

class BoekLendingException(BoekAPIException):
    """Raised when there is an error processing lending logic."""
    pass

class BoekReturnException(BoekAPIException):
    """Raised when there is an error processing return logic."""
    pass