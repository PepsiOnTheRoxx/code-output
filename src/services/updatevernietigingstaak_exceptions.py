class UpdateVernietigingstaakException(Exception):
    """Base exception for UpdateVernietigingstaak feature."""
    pass

class VernietigingstaakNotFoundException(UpdateVernietigingstaakException):
    """Raised when the specified Vernietigingstaak does not exist."""
    pass

class InvalidVernietigingstaakDataException(UpdateVernietigingstaakException):
    """Raised when the provided data for updating is invalid."""
    pass

class VernietigingstaakUpdateNotAllowedException(UpdateVernietigingstaakException):
    """Raised when the update operation is not allowed."""
    pass

class VernietigingstaakServiceException(UpdateVernietigingstaakException):
    """Raised when an unexpected error occurs in the VernietigingstaakService."""
    pass