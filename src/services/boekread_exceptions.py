class BoekReadException(Exception):
    """Basis exception voor BoekRead fouten."""
    pass

class BoekNietGevondenException(BoekReadException):
    """Exception wanneer een boek niet wordt gevonden in de database."""
    pass

class BoekDatabaseFoutException(BoekReadException):
    """Exception bij algemene database fouten tijdens ophalen van boeken."""
    pass

class BoekOphalenOnbekendeFoutException(BoekReadException):
    """Exception voor onbekende fouten tijdens het ophalen van boeken."""
    pass
