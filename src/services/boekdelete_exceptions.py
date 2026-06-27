class BoekDeleteException(Exception):
    """Base exception for BoekDelete feature."""
    pass

class BoekNietGevondenException(BoekDeleteException):
    """Boek niet gevonden voor verwijderen."""
    pass

class BoekNotFoundException(BoekNietGevondenException):
    """Alias zodat import werkt."""
    pass

class DeleteNotAllowedException(BoekDeleteException):
    pass

class BoekVerwijderPermissionDeniedException(BoekDeleteException):
    """Gebruiker heeft geen permissie om boek te verwijderen."""
    pass

class BoekVerwijderConflictException(BoekDeleteException):
    """Verwijderen van boek veroorzaakt een conflict (bijv. boek in gebruik)."""
    pass

class BoekVerwijderDatabaseException(BoekDeleteException):
    """Database error bij verwijderen boek."""
    pass
