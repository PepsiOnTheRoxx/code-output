class DeleteVernietigingstaakError(Exception):
    """Base exception for DeleteVernietigingstaak feature."""
    pass

class VernietigingstaakNotFoundException(DeleteVernietigingstaakError):
    """Raised when the Vernietigingstaak to delete is not found."""
    pass

class UnauthorizedVernietigingstaakDeleteException(DeleteVernietigingstaakError):
    """Raised when the user does not have permission to delete the Vernietigingstaak."""
    pass

class VernietigingstaakDeleteException(DeleteVernietigingstaakError):
    """Raised when the Vernietigingstaak cannot be deleted due to existing dependencies or error."""
    pass

# Legacy aliases for compatibility
def VernietigingstaakNotFoundError(*args, **kwargs):
    return VernietigingstaakNotFoundException(*args, **kwargs)

def VernietigingstaakDeletePermissionError(*args, **kwargs):
    return UnauthorizedVernietigingstaakDeleteException(*args, **kwargs)

def VernietigingstaakDeleteDependencyError(*args, **kwargs):
    return VernietigingstaakDeleteException(*args, **kwargs)

def VernietigingstaakDeleteValidationError(*args, **kwargs):
    return ValueError(*args, **kwargs)

def VernietigingstaakDeleteDatabaseError(*args, **kwargs):
    return VernietigingstaakDeleteException(*args, **kwargs)
