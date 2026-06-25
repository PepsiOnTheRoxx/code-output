class BoekUpdateException(Exception):
    """Basisklasse voor uitzonderingen in de BoekUpdate feature."""
    pass

class BoekNietGevondenException(BoekUpdateException):
    """Boek kon niet gevonden worden."""
    pass

class OngeldigeBoekDataException(BoekUpdateException):
    """De verstrekte boekdata is ongeldig."""
    pass

class BoekUpdateMisluktException(BoekUpdateException):
    """Bijwerken van het boek is mislukt."""
    pass

class BoekUpdateNietToegestaanException(BoekUpdateException):
    """De update actie voor het boek is niet toegestaan."""
    pass