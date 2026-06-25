class BoekUpdateException(Exception):
    """Basisexception voor alle BoekUpdate gerelateerde fouten."""
    pass

class BoekNietGevondenException(BoekUpdateException):
    """Exception wanneer het boek niet gevonden wordt in de database."""
    pass

class OngeldigeBoekDataException(BoekUpdateException):
    """Exception voor ongeldige of incomplete boekdata tijdens updaten."""
    pass

class DatabaseUpdateFoutException(BoekUpdateException):
    """Exception bij fouten tijdens het wegschrijven van de update in de database."""
    pass

class GeenWijzigingenGedetecteerdException(BoekUpdateException):
    """Exception wanneer er geen wijzigingen zijn tussen oude en nieuwe boekdata."""
    pass