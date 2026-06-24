class LinkVTBehandelaarException(Exception):
    """Base exception for LinkVTBehandelaar feature."""
    pass

class LinkVTBehandelaarVernietigingstaakNotFound(LinkVTBehandelaarException):
    """Raised when the specified Vernietigingstaak is not found."""
    pass

class LinkVTBehandelaarGebruikerNotFound(LinkVTBehandelaarException):
    """Raised when the specified Gebruiker is not found."""
    pass

class LinkVTBehandelaarAlreadyLinked(LinkVTBehandelaarException):
    """Raised when the Gebruiker is already linked as Behandelaar to the Vernietigingstaak."""
    pass

class LinkVTBehandelaarNotAllowed(LinkVTBehandelaarException):
    """Raised when linking the Gebruiker as Behandelaar to the Vernietigingstaak is not allowed."""
    pass

class LinkVTBehandelaarInvalidInput(LinkVTBehandelaarException):
    """Raised when input data for linking is invalid."""
    pass

class LinkVTBehandelaarRelationFailed(LinkVTBehandelaarException):
    """Raised when the relation creation between Gebruiker and Vernietigingstaak fails."""
    pass
