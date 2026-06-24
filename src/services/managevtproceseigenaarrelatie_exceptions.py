class ManageVTProceseigenaarRelatieException(Exception):
    """Base exception for ManageVTProceseigenaarRelatie errors."""
    pass

class VTProceseigenaarRelatieNotFoundException(ManageVTProceseigenaarRelatieException):
    """Raised when the VTProceseigenaarRelatie does not exist."""
    pass

class VTProceseigenaarRelatieAlreadyExistsException(ManageVTProceseigenaarRelatieException):
    """Raised when the VTProceseigenaarRelatie already exists."""
    pass

class InvalidVTProceseigenaarRelatieException(ManageVTProceseigenaarRelatieException):
    """Raised when provided data for VTProceseigenaarRelatie is invalid."""
    pass

class VTProceseigenaarRelatieUpdateFailedException(ManageVTProceseigenaarRelatieException):
    """Raised when updating the VTProceseigenaarRelatie fails."""
    pass

class VTProceseigenaarRelatieDeleteFailedException(ManageVTProceseigenaarRelatieException):
    """Raised when deleting the VTProceseigenaarRelatie fails."""
    pass