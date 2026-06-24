class LinkVTArchivarisException(Exception):
    """Base exception for LinkVTArchivaris feature."""
    pass

class ArchivarisAlreadyLinkedException(LinkVTArchivarisException):
    """Raised when the Gebruiker is already linked as Archivaris to the Vernietigingstaak."""
    pass

class ArchivarisNotFoundException(LinkVTArchivarisException):
    """Raised when the specified Archivaris (Gebruiker) cannot be found."""
    pass

class VernietigingstaakNotFoundException(LinkVTArchivarisException):
    """Raised when the specified Vernietigingstaak cannot be found."""
    pass

class InvalidArchivarisRoleException(LinkVTArchivarisException):
    """Raised when the Gebruiker does not have the required Archivaris role."""
    pass

class LinkOperationNotAllowedException(LinkVTArchivarisException):
    """Raised when linking an Archivaris to the Vernietigingstaak is not allowed due to business rules."""
    pass