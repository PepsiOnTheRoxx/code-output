class VTArchivarisRelatieAPIException(Exception):
    """Base exception for VTArchivarisRelatieAPI errors."""
    pass

class VTArchivarisRelatieAPINotFound(VTArchivarisRelatieAPIException):
    """Raised when a VTArchivaris-relatie is not found."""
    pass

class VTArchivarisRelatieAPIInvalidInput(VTArchivarisRelatieAPIException):
    """Raised when input data is invalid for VTArchivaris-relatie."""
    pass

class VTArchivarisRelatieAPIPermissionDenied(VTArchivarisRelatieAPIException):
    """Raised when action is not allowed on VTArchivaris-relatie."""
    pass

class VTArchivarisRelatieAPIConflict(VTArchivarisRelatieAPIException):
    """Raised when there is a conflict in VTArchivaris-relatie operation."""
    pass

class VTArchivarisRelatieAPIInternalError(VTArchivarisRelatieAPIException):
    """Raised for internal errors in VTArchivaris-relatie API."""
    pass