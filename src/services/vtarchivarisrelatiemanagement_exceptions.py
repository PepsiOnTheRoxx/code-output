class VTArchivarisRelatieServiceException(Exception):
    """Base exception for VTArchivarisRelatieService related errors."""
    pass

class ArchivarisKoppelingBestaatAlException(VTArchivarisRelatieServiceException):
    """Raised when a coupling between Vernietigingstaak and Archivaris already exists."""
    pass

class ArchivarisNietGevondenException(VTArchivarisRelatieServiceException):
    """Raised when the specified Archivaris user does not exist."""
    pass

class VernietigingstaakNietGevondenException(VTArchivarisRelatieServiceException):
    """Raised when the specified Vernietigingstaak does not exist."""
    pass

class ArchivarisKoppelingNietGevondenException(VTArchivarisRelatieServiceException):
    """Raised when the requested Archivaris-Vernietigingstaak relation could not be found."""
    pass

class ArchivarisKoppelingVerwijderenNietToegestaanException(VTArchivarisRelatieServiceException):
    """Raised when it's not permitted to remove the Archivaris relation from Vernietigingstaak."""
    pass