class ManageVTBehandelaarRelatieException(Exception):
    """Base exception for ManageVTBehandelaarRelatie feature."""
    pass

class VTBehandelaarRelatieNotFound(ManageVTBehandelaarRelatieException):
    """Raised when a VTBehandelaar-relatie is not found."""
    pass

class VTBehandelaarRelatieAlreadyExists(ManageVTBehandelaarRelatieException):
    """Raised when a VTBehandelaar-relatie already exists."""
    pass

class InvalidVTBehandelaarRelatieData(ManageVTBehandelaarRelatieException):
    """Raised when the supplied data for VTBehandelaar-relatie is invalid."""
    pass

class UnauthorizedVTBehandelaarRelatieAccess(ManageVTBehandelaarRelatieException):
    """Raised when the user is not authorized to access the VTBehandelaar-relatie."""
    pass

class VTBehandelaarRelatieDeleteError(ManageVTBehandelaarRelatieException):
    """Raised when an error occurs while deleting a VTBehandelaar-relatie."""
    pass

class VTBehandelaarRelatieUpdateError(ManageVTBehandelaarRelatieException):
    """Raised when an error occurs while updating a VTBehandelaar-relatie."""
    pass