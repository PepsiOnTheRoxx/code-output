class VTProceseigenaarRelatieAPIException(Exception):
    """Base exception for VTProceseigenaarRelatieAPI errors."""
    pass

class VTProceseigenaarRelatieAPINotFoundException(VTProceseigenaarRelatieAPIException):
    """Raised when a requested resource is not found."""
    pass

class VTProceseigenaarRelatieAPIValidationException(VTProceseigenaarRelatieAPIException):
    """Raised when data validation fails."""
    pass

class VTProceseigenaarRelatieAPIConflictException(VTProceseigenaarRelatieAPIException):
    """Raised when there is a conflict, e.g., on unique constraints."""
    pass

class VTProceseigenaarRelatieAPIUnauthorizedException(VTProceseigenaarRelatieAPIException):
    """Raised when authentication or authorization has failed."""
    pass

class VTProceseigenaarRelatieAPIDatabaseException(VTProceseigenaarRelatieAPIException):
    """Raised for database-related errors."""
    pass

class VTProceseigenaarRelatieAPIFactTypeException(VTProceseigenaarRelatieAPIException):
    """Raised for FactType (ElementID: 5) related errors."""
    pass