class DeleteVernietigingstaakError(Exception):
    """Base exception for DeleteVernietigingstaak feature."""
    pass

class VernietigingstaakNotFoundError(DeleteVernietigingstaakError):
    """Raised when the Vernietigingstaak to delete does not exist."""
    pass

class DeleteVernietigingstaakPermissionError(DeleteVernietigingstaakError):
    """Raised when the user has no permission to delete the Vernietigingstaak."""
    pass

class DeleteVernietigingstaakIntegrityError(DeleteVernietigingstaakError):
    """Raised when the Vernietigingstaak cannot be deleted due to integrity reasons."""
    pass

class DeleteVernietigingstaakValidationError(DeleteVernietigingstaakError):
    """Raised when the provided data for deletion is invalid."""
    pass

class DeleteVernietigingstaakDependencyError(DeleteVernietigingstaakError):
    """Raised when the Vernietigingstaak cannot be deleted due to dependent records."""
    pass