class VTArchivarisRelatieServiceException(Exception):
    """Base exception for VTArchivarisRelatieService related errors."""
    pass

class RelatieBestaatAlException(VTArchivarisRelatieServiceException):
    """Raised when a coupling between Vernietigingstaak and Archivaris already exists."""
    pass

class RelatieNietGevondenException(VTArchivarisRelatieServiceException):
    """Raised when the requested Archivaris-Vernietigingstaak relation could not be found."""
    pass

class OngeldigeInputException(VTArchivarisRelatieServiceException):
    """Raised when input is invalid"""
    pass
