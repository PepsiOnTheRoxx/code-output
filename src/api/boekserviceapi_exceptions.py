class BoekAPIException(Exception):
    """Basisklasse voor BoekAPI gerelateerde exceptions."""
    pass

class BoekNietGevondenException(BoekAPIException):
    """Exception voor wanneer een boek niet gevonden wordt (EN: BoekNotFoundException)."""
    pass

class OngeldigeBoekDataException(BoekAPIException):
    """Exception voor wanneer de geleverde boekdata ongeldig is."""
    pass

class BoekAanmakenMisluktException(BoekAPIException):
    """Exception voor wanneer het aanmaken van een boek faalt."""
    pass

class BoekBijwerkenMisluktException(BoekAPIException):
    """Exception voor wanneer het bijwerken van een boek faalt."""
    pass

class BoekVerwijderenMisluktException(BoekAPIException):
    """Exception voor wanneer het verwijderen van een boek faalt."""
    pass

# Dummy BoekService class maken zodat patchen altijd werkt. Hoort alleen hier te staan voor patching!
class BoekService:
    def __init__(self, conn):
        pass
