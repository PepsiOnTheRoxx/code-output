class VTBehandelaarRelatieException(Exception):
    """Base exception for VTBehandelaarRelatieService errors."""
    pass

class VTBehandelaarRelatieNotFoundException(VTBehandelaarRelatieException):
    """Raised when the requested BehandelaarRelatie is not found."""
    pass

class VTBehandelaarRelatieAlreadyExistsException(VTBehandelaarRelatieException):
    """Raised when attempting to create a duplicate BehandelaarRelatie."""
    pass

class VTBehandelaarRelatieInvalidDataException(VTBehandelaarRelatieException):
    """Raised when provided data for BehandelaarRelatie is invalid."""
    pass

class VTBehandelaarRelatiePermissionException(VTBehandelaarRelatieException):
    """Raised when an operation is not permitted for the current user."""
    pass

class VTBehandelaarRelatieFactTypeException(VTBehandelaarRelatieException):
    """Raised on errors related to FactType (ElementID: 4) interactions."""
    pass