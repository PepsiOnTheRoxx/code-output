class VTProceseigenaarRelatieAPIException(Exception):
    """Base exception for VTProceseigenaarRelatieAPI errors."""
    pass

class VTProceseigenaarRelatieNotFoundException(VTProceseigenaarRelatieAPIException):
    """Raised when a requested VTProceseigenaar-relatie is not found."""
    pass

class VTProceseigenaarRelatieValidationException(VTProceseigenaarRelatieAPIException):
    """Raised when validation fails for a VTProceseigenaar-relatie request."""
    pass

class VTProceseigenaarRelatieConflictException(VTProceseigenaarRelatieAPIException):
    """Raised when there is a conflict in VTProceseigenaar-relatie (e.g., duplicate entry)."""
    pass

class VTProceseigenaarRelatiePermissionDeniedException(VTProceseigenaarRelatieAPIException):
    """Raised when permission for VTProceseigenaar-relatie API is denied."""
    pass

class VTProceseigenaarRelatieMetamodelException(VTProceseigenaarRelatieAPIException):
    """Raised when a metamodel issue occurs with VTProceseigenaar-relatie processing."""
    pass