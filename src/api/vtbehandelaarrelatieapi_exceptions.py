class VTBehandelaarRelatieAPIException(Exception):
    """Base exception for VTBehandelaarRelatieAPI errors."""
    pass

# --- The following are not used/needed for this API/tests ---
class BehandelaarNotFoundException(VTBehandelaarRelatieAPIException):
    pass
class InvalidBehandelaarRelatieDataException(VTBehandelaarRelatieAPIException):
    pass
class BehandelaarRelatieAlreadyExistsException(VTBehandelaarRelatieAPIException):
    pass
class UnauthorizedBehandelaarRelatieAccessException(VTBehandelaarRelatieAPIException):
    pass
class BehandelaarRelatieAPIDatabaseException(VTBehandelaarRelatieAPIException):
    pass

# --- These are needed for the API/tests and will be used ---
class VTBehandelaarRelatieNotFound(VTBehandelaarRelatieAPIException):
    """Raised when the behandelaar relatie is not found."""
    pass

class VTBehandelaarRelatieInvalidData(VTBehandelaarRelatieAPIException):
    """Raised when provided data for behandelaar relatie is invalid."""
    pass
