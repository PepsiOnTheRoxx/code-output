class BoekAPIException(Exception):
    """Base exception for BoekAPI component."""
    pass

class BoekNotFoundException(BoekAPIException):
    """Raised when a requested boek is not found."""
    pass

class BoekValidationException(BoekAPIException):
    """Raised when validation fails for a boek."""
    pass

class BoekCreationException(BoekAPIException):
    """Raised when creation of a boek fails."""
    pass

class BoekUpdateException(BoekAPIException):
    """Raised when update of a boek fails."""
    pass

class BoekDeleteException(BoekAPIException):
    """Raised when deletion of a boek fails."""
    pass

class BoekInterfaceNotFoundException(BoekAPIException):
    """Raised when a specific boek-interface route is not found."""
    pass
