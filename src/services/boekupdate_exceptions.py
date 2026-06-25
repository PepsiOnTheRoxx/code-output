class BoekUpdateException(Exception):
    """Basis-exceptie voor BoekUpdate-feature."""
    pass

class BoekNietGevondenException(BoekUpdateException):
    """Boek met opgegeven ID is niet gevonden."""
    pass

class OngeldigeBoekDataException(BoekUpdateException):
    """De aangeleverde boekdata is ongeldig."""
    pass

class DatabaseUpdateFoutException(BoekUpdateException):
    """Er is een fout opgetreden tijdens het bijwerken van de database."""
    pass

class GeenWijzigingenGedetecteerdException(BoekUpdateException):
    """Er zijn geen wijzigingen om op te slaan."""
    pass
