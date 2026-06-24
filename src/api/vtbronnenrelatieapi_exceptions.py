class VTBronnenRelatieAPIException(Exception):
    """Base exception for VTBronnenRelatieAPI errors."""
    pass

class VTBronnenRelatieAPINotFoundException(VTBronnenRelatieAPIException):
    """Raised when a VTBronnen-relatie is not found."""
    pass

class VTBronnenRelatieAPIValidationException(VTBronnenRelatieAPIException):
    """Raised when validation fails in VTBronnenRelatieAPI."""
    pass

class VTBronnenRelatieAPIPermissionException(VTBronnenRelatieAPIException):
    """Raised when user lacks permission for VTBronnen-relatie operation."""
    pass

class VTBronnenRelatieAPIConflictException(VTBronnenRelatieAPIException):
    """Raised when a VTBronnen-relatie conflict occurs."""
    pass

class VTBronnenRelatieAPIDatabaseException(VTBronnenRelatieAPIException):
    """Raised on internal database errors for VTBronnen-relatie."""
    pass