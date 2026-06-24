class ReadVernietigingstaakException(Exception):
    """Base exception for VernietigingstaakService read operations."""
    pass

class VernietigingstaakNotFoundException(ReadVernietigingstaakException):
    """Raised when the requested Vernietigingstaak could not be found."""
    pass

class VernietigingstaakPermissionDeniedException(ReadVernietigingstaakException):
    """Raised when permission is denied for reading the Vernietigingstaak."""
    pass

class VernietigingstaakInvalidInputException(ReadVernietigingstaakException):
    """Raised when provided input for reading Vernietigingstaak is invalid."""
    pass

class VernietigingstaakMetamodelMismatchException(ReadVernietigingstaakException):
    """Raised when the Vernietigingstaak does not match the expected metamodel."""
    pass

class VernietigingstaakServiceUnavailableException(ReadVernietigingstaakException):
    """Raised when the VernietigingstaakService is unavailable."""
    pass