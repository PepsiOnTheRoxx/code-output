class BoekDeleteException(Exception):
    """Basisklasse voor exceptions in de BoekDelete feature."""
    pass

class BoekNotFoundException(BoekDeleteException):
    """Exception als het opgegeven Boek niet gevonden wordt."""
    pass

class BoekDeletePermissionException(BoekDeleteException):
    """Exception als er onvoldoende rechten zijn om een Boek te verwijderen."""
    pass

class BoekDeleteDatabaseException(BoekDeleteException):
    """Exception bij een databasefout tijdens verwijderen van een Boek."""
    pass

class BoekDeleteIntegrityException(BoekDeleteException):
    """Exception als integriteitsbeperkingen verwijderen van het Boek verhinderen."""
    pass