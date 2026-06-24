class DeleteVernietigingstaakError(Exception):
    """Base exception for DeleteVernietigingstaak feature."""
    pass

class VernietigingstaakNotFoundError(DeleteVernietigingstaakError):
    """Raised when the Vernietigingstaak to delete is not found."""
    pass

class VernietigingstaakDeletePermissionError(DeleteVernietigingstaakError):
    """Raised when the user does not have permission to delete the Vernietigingstaak."""
    pass

class VernietigingstaakDeleteDependencyError(DeleteVernietigingstaakError):
    """Raised when the Vernietigingstaak cannot be deleted due to existing dependencies."""
    pass

class VernietigingstaakDeleteValidationError(DeleteVernietigingstaakError):
    """Raised if Vernietigingstaak delete input or state is invalid."""
    pass

class VernietigingstaakDeleteDatabaseError(DeleteVernietigingstaakError):
    """Raised when a database error occurs during deletion of the Vernietigingstaak."""
    pass