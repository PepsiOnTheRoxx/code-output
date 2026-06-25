class BoekDeleteException(Exception):
    """Base exception for BoekDelete feature in BoekService."""
    pass

class BoekNietGevondenException(BoekDeleteException):
    """Raised when the boek to delete is not found."""
    pass

class BoekDeleteMisluktException(BoekDeleteException):
    """Raised when the deletion of a boek fails."""
    pass

class OngeldigeBoekIdException(BoekDeleteException):
    """Raised when an invalid boek id is provided."""
    pass