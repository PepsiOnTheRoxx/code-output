class ManageVTArchivarisRelatieException(Exception):
    """Base exception for ManageVTArchivarisRelatie feature."""
    pass

class VTArchivarisRelatieNotFoundException(ManageVTArchivarisRelatieException):
    """Raised when the VTArchivaris-relatie is not found."""
    pass

class VTArchivarisRelatieAlreadyExistsException(ManageVTArchivarisRelatieException):
    """Raised when the VTArchivaris-relatie already exists."""
    pass

class InvalidVTArchivarisRelatieDataException(ManageVTArchivarisRelatieException):
    """Raised when provided data for VTArchivaris-relatie is invalid."""
    pass

class UnauthorizedVTArchivarisRelatieActionException(ManageVTArchivarisRelatieException):
    """Raised when an action is not authorized on VTArchivaris-relatie."""
    pass

class VTArchivarisRelatieOperationFailedException(ManageVTArchivarisRelatieException):
    """Raised when an operation on VTArchivaris-relatie fails."""
    pass