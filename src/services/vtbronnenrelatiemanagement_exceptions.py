class VTBronnenRelatieServiceException(Exception):
    """Base exception for VTBronnenRelatieService errors."""
    pass

class VTBronnenRelatieNotFoundException(VTBronnenRelatieServiceException):
    """Raised when a requested VTBronnenRelatie is not found."""
    pass

class VTBronnenRelatieAlreadyExistsException(VTBronnenRelatieServiceException):
    """Raised when trying to create a VTBronnenRelatie that already exists."""
    pass

class VTBronnenRelatieInvalidStateException(VTBronnenRelatieServiceException):
    """Raised when the VTBronnenRelatie is in an invalid state for the requested operation."""
    pass

class VTBronnenRelatieValidationException(VTBronnenRelatieServiceException):
    """Raised when data validation fails for a VTBronnenRelatie operation."""
    pass

class VTBronnenRelatiePersistenceException(VTBronnenRelatieServiceException):
    """Raised when data persistence fails in VTBronnenRelatieService."""
    pass