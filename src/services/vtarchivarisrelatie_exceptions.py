class VTArchivarisRelatieException(Exception):
    """Base exception for VTArchivarisRelatieService."""

class VTArchivarisRelatieNotFoundException(VTArchivarisRelatieException):
    """Raised when the archivaris relation is not found."""

class VTArchivarisRelatieAlreadyExistsException(VTArchivarisRelatieException):
    """Raised when the archivaris relation already exists."""

class VTArchivarisRelatieInvalidUserException(VTArchivarisRelatieException):
    """Raised when an invalid user is specified."""

class VTArchivarisRelatieInvalidTaakException(VTArchivarisRelatieException):
    """Raised when an invalid vernietigingstaak is specified."""

class VTArchivarisRelatiePermissionDeniedException(VTArchivarisRelatieException):
    """Raised when user has insufficient rights for an operation."""

class VTArchivarisRelatieFactTypeMismatchException(VTArchivarisRelatieException):
    """Raised when an invalid FactType (element: 6) relation is encountered."""
