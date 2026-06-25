class BoekReadException(Exception):
    """Basisklasse voor BoekRead exceptions."""
    pass

class BoekNietGevondenException(BoekReadException):
    """Boek niet gevonden in de database."""
    pass

class BoekLijstLeegException(BoekReadException):
    """Geen boeken gevonden in de database."""
    pass

class BoekDatabaseFoutException(BoekReadException):
    """Algemene databasefout bij het ophalen van boeken."""
    pass

class OngeldigBoekIDException(BoekReadException):
    """Ongeldig of corrupt boek-ID opgegeven."""
    pass