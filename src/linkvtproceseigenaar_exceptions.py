class LinkVTProceseigenaarException(Exception):
    """Base exception for LinkVTProceseigenaar feature."""
    pass

class ProceseigenaarAlreadyLinkedException(LinkVTProceseigenaarException):
    """Raised when the proceseigenaar is already linked to the vernietigingstaak."""
    pass

class ProceseigenaarNotFoundException(LinkVTProceseigenaarException):
    """Raised when the specified proceseigenaar (gebruiker) does not exist."""
    pass

class VernietigingstaakNotFoundException(LinkVTProceseigenaarException):
    """Raised when the specified vernietigingstaak does not exist."""
    pass

class FactTypeMismatchException(LinkVTProceseigenaarException):
    """Raised when the FactType element does not match the expected specification."""
    pass

class LinkVTProceseigenaarPermissionDeniedException(LinkVTProceseigenaarException):
    """Raised when the user does not have permission to relate a proceseigenaar to a vernietigingstaak."""
    pass

class InvalidLinkVTProceseigenaarInputException(LinkVTProceseigenaarException):
    """Raised when input values for linking a proceseigenaar are invalid."""
    pass

# Toevoeging: aliases naar 'Nederlands'-stijl exceptions tbv main code/tests compatibility
class GebruikerNietGevondenException(ProceseigenaarNotFoundException):
    pass

class TaakNietGevondenException(VernietigingstaakNotFoundException):
    pass

class ProceseigenaarAlGekoppeldException(ProceseigenaarAlreadyLinkedException):
    pass

class OngeldigeRelatieException(InvalidLinkVTProceseigenaarInputException):
    pass
