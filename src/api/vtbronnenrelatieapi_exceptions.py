class VTBronnenRelatieAPIException(Exception):
    """Base exception for VTBronnenRelatieAPI component."""
    pass

class VTBronnenRelatieNotFoundException(VTBronnenRelatieAPIException):
    """Exception raised when a requested Bron or Relatie is not found."""
    pass

class VTBronnenRelatieValidationException(VTBronnenRelatieAPIException):
    """Exception raised for invalid input data in Bronnen-koppeling."""
    pass
