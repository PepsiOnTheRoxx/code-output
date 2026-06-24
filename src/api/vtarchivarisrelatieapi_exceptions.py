class VTArchivarisRelatieAPIException(Exception):
    """Base exception for VTArchivarisRelatieAPI errors."""
    pass

# EXCEPTIONS USED IN IMPLEMENTATION AND TESTS
class VTArchivarisRelatieNotFound(VTArchivarisRelatieAPIException):
    """Raised when a requested resource is not found in VTArchivarisRelatieAPI."""
    pass

class VTArchivarisRelatieValidationError(VTArchivarisRelatieAPIException):
    """Raised when validation of input or data fails in VTArchivarisRelatieAPI."""
    pass

class VTArchivarisRelatieAPIConflictException(VTArchivarisRelatieAPIException):
    """Raised when there is a conflict, such as duplicate entry, in VTArchivarisRelatieAPI."""
    pass

class VTArchivarisRelatieAPIUnauthorizedException(VTArchivarisRelatieAPIException):
    """Raised when authorization fails in VTArchivarisRelatieAPI."""
    pass

class VTArchivarisRelatieAPIInternalException(VTArchivarisRelatieAPIException):
    """Raised when an internal error occurs within VTArchivarisRelatieAPI."""
    pass
