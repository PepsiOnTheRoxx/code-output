class VernietigingstaakUpdateException(Exception):
    """Basisklasse voor alle VernietigingstaakUpdate exceptions."""
    pass

class VernietigingstaakNietGevondenException(VernietigingstaakUpdateException):
    """Vernietigingstaak bestaat niet."""
    pass

class VernietigingstaakOngeldigeStatusException(VernietigingstaakUpdateException):
    """De status van Vernietigingstaak staat wijziging niet toe."""
    pass

class VernietigingstaakValidatieException(VernietigingstaakUpdateException):
    """Validatie van Vernietigingstaak update is mislukt."""
    pass

class VernietigingstaakOnvoldoendeRechtenException(VernietigingstaakUpdateException):
    """Gebruiker heeft onvoldoende rechten voor deze wijziging."""
    pass

class VernietigingstaakUpdateConflictException(VernietigingstaakUpdateException):
    """Er is een conflict bij het updaten van de Vernietigingstaak."""
    pass