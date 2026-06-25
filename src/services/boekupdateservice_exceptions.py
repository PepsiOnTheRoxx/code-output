class BoekUpdateServiceException(Exception):
    """Basisklasse voor BoekUpdateService fouten."""
    pass

class BoekNietGevondenException(BoekUpdateServiceException):
    """Opgeworpen wanneer het Boek niet in de database wordt gevonden."""
    pass

class OngeldigeBoekDataException(BoekUpdateServiceException):
    """Opgeworpen wanneer de aangeleverde Boek data ongeldig is."""
    pass

class BoekUpdateMisluktException(BoekUpdateServiceException):
    """Opgeworpen wanneer het wijzigen van het Boek niet lukt."""
    pass

class BoekServiceDatabaseException(BoekUpdateServiceException):
    """Opgeworpen bij een database fout in BoekService."""
    pass