class BoekSeederException(Exception):
    """Basisklasse voor alle BoekSeeder exceptions."""
    pass

class BoekSeederMinimumAantalException(BoekSeederException):
    """Exception wanneer minder dan 5 boeken worden toegevoegd."""
    pass

class BoekSeederDatabaseException(BoekSeederException):
    """Exception bij een fout tijdens database interactie."""
    pass

class BoekSeederServiceException(BoekSeederException):
    """Exception bij een fout vanuit de service laag."""
    pass
