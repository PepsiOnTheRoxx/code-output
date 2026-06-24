class LinkVTBronnenException(Exception):
    """Base exception for LinkVTBronnen feature."""
    pass

class BronNotFoundException(LinkVTBronnenException):
    """Raised when the specified Bron cannot be found."""
    pass

class VernietigingstaakNotFoundException(LinkVTBronnenException):
    """Raised when the specified Vernietigingstaak cannot be found."""
    pass

class BronAlreadyLinkedException(LinkVTBronnenException):
    """Raised when trying to link a Bron that is already related."""
    pass

class InvalidBronTypeException(LinkVTBronnenException):
    """Raised when the Bron type is invalid for linking."""
    pass

class InvalidVernietigingstaakStateException(LinkVTBronnenException):
    """Raised when the Vernietigingstaak is in a state that cannot accept new Bron relations."""
    pass

class LinkCreationFailedException(LinkVTBronnenException):
    """Raised when the relation between Bron and Vernietigingstaak cannot be created."""
    pass

class LinkDeleteNotAllowedException(LinkVTBronnenException):
    """Raised when unlinking a Bron from a Vernietigingstaak is not allowed."""
    pass