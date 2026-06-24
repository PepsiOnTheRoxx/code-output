class VernietigingstaakDeleteException(Exception):
    """Base exception for VernietigingstaakDelete feature."""
    pass

class VernietigingstaakNotFoundException(VernietigingstaakDeleteException):
    """Raised when the Vernietigingstaak to delete is not found."""
    pass

class VernietigingstaakDeletePermissionException(VernietigingstaakDeleteException):
    """Raised when delete permission is denied."""
    pass

class VernietigingstaakDeleteDependencyException(VernietigingstaakDeleteException):
    """Raised when the Vernietigingstaak cannot be deleted due to dependencies."""
    pass

class VernietigingstaakDeleteDatabaseException(VernietigingstaakDeleteException):
    """Raised on database errors during delete."""
    pass

class VernietigingstaakDeleteInvalidStateException(VernietigingstaakDeleteException):
    """Raised when Vernietigingstaak is in an invalid state for deletion."""
    pass
