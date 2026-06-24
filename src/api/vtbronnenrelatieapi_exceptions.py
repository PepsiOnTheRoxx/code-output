class VTBronnenRelatieAPIException(Exception):
    """Base exception for VTBronnenRelatieAPI component."""
    pass

class VTBronnenRelatieAPINotFound(VTBronnenRelatieAPIException):
    """Exception raised when a requested Bron or Relatie is not found."""
    pass

class VTBronnenRelatieAPIInvalidInput(VTBronnenRelatieAPIException):
    """Exception raised for invalid input data in Bronnen-koppeling."""
    pass

class VTBronnenRelatieAPIConflict(VTBronnenRelatieAPIException):
    """Exception raised when there is a conflict in Bronnen-koppeling data."""
    pass

class VTBronnenRelatieAPIUnauthorized(VTBronnenRelatieAPIException):
    """Exception raised when authorization fails."""
    pass

class VTBronnenRelatieAPIInternalError(VTBronnenRelatieAPIException):
    """Exception raised for unexpected internal errors in the API."""
    pass