class BoekSeederServiceException(Exception):
    """Basisklasse voor alle BoekSeederService gerelateerde exceptions."""
    pass

class DatabaseInitialisatieFout(BoekSeederServiceException):
    """Fout opgetreden tijdens initialisatie van de database."""
    pass

class DatabaseConnectieFout(BoekSeederServiceException):
    """Fout bij het verbinden met de database."""
    pass

class BoekenInsertieFout(BoekSeederServiceException):
    """Fout opgetreden bij het inserten van dummy boeken."""
    pass

class OngeldigBoekGegevensFout(BoekSeederServiceException):
    """Boekgegevens voldoen niet aan het verwachte formaat."""
    pass
