class VTBronnenRelatieException(Exception):
    """Base exception for VTBronnenRelatieService errors."""


class VTBronnenRelatieNotFoundException(VTBronnenRelatieException):
    """Raised when a requested VTBronnenRelatie does not exist."""


class VTBronnenRelatieAlreadyExistsException(VTBronnenRelatieException):
    """Raised when attempting to create a VTBronnenRelatie that already exists."""


class InvalidVTBronnenRelatieException(VTBronnenRelatieException):
    """Raised when provided data for VTBronnenRelatie is invalid."""


class VTBronnenRelatieDependencyException(VTBronnenRelatieException):
    """Raised when there is a dependency error with Bron or Vernietigingstaak."""


class VTBronnenRelatieOperationException(VTBronnenRelatieException):
    """Raised when a generic operation on VTBronnenRelatie fails."""