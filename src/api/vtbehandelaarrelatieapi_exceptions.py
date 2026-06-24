class VTBehandelaarRelatieAPIException(Exception):
    """Base exception for VTBehandelaarRelatieAPI errors."""
    pass

class BehandelaarNotFoundException(VTBehandelaarRelatieAPIException):
    """Raised when a behandelaar (practitioner) could not be found."""
    pass

class InvalidBehandelaarRelatieDataException(VTBehandelaarRelatieAPIException):
    """Raised when provided data for behandelaar relatie is invalid."""
    pass

class BehandelaarRelatieAlreadyExistsException(VTBehandelaarRelatieAPIException):
    """Raised when a requested behandelaar relatie already exists."""
    pass

class UnauthorizedBehandelaarRelatieAccessException(VTBehandelaarRelatieAPIException):
    """Raised when user is not authorized to access behandelaar relatie."""
    pass

class BehandelaarRelatieAPIDatabaseException(VTBehandelaarRelatieAPIException):
    """Raised on database errors in VTBehandelaarRelatieAPI."""
    pass