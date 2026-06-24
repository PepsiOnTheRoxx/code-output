class ManageVTBronnenRelatieException(Exception):
    """Base exception for ManageVTBronnenRelatie feature."""
    pass

class VTBronnenRelatieNotFoundException(ManageVTBronnenRelatieException):
    """Raised when the requested VTBronnen-relatie is not found."""
    pass

class VTBronnenRelatieAlreadyExistsException(ManageVTBronnenRelatieException):
    """Raised when trying to create a VTBronnen-relatie that already exists."""
    pass

class InvalidVTBronnenRelatieStateException(ManageVTBronnenRelatieException):
    """Raised when the VTBronnen-relatie is in an invalid state for the attempted operation."""
    pass

class VTBronnenRelatieUpdateException(ManageVTBronnenRelatieException):
    """Raised when an error occurs during update of a VTBronnen-relatie."""
    pass

class VTBronnenRelatieDeleteException(ManageVTBronnenRelatieException):
    """Raised when an error occurs during deletion of a VTBronnen-relatie."""
    pass

class VTBronnenRelatieValidationException(ManageVTBronnenRelatieException):
    """Raised when validation fails for a VTBronnen-relatie."""
    pass
