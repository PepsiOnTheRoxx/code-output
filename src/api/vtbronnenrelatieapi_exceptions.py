class VTBronnenRelatieAPIException(Exception):
    """Base exception for VTBronnenRelatieAPI errors."""
    pass

class VTBronnenRelatieNotFound(VTBronnenRelatieAPIException):
    """Raised when a VTBronnen-relatie is not found."""
    pass

class VTBronnenRelatieInvalidData(VTBronnenRelatieAPIException):
    """Raised when validation fails in VTBronnenRelatieAPI."""
    pass

class VTBronnenRelatieAlreadyExists(VTBronnenRelatieAPIException):
    """Raised when a VTBronnen-relatie conflict occurs."""
    pass

class VTBronnenRelatieDatabaseError(VTBronnenRelatieAPIException):
    """Raised on internal database errors for VTBronnen-relatie."""
    pass
