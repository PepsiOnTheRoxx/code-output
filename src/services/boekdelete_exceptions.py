class BoekDeleteException(Exception):
    """Basisklasse voor alle BoekDelete exceptions."""
    pass

class BoekNietGevondenException(BoekDeleteException):
    """Opgegooid wanneer het te verwijderen boek niet gevonden wordt."""
    pass

class BoekDeleteDatabaseException(BoekDeleteException):
    """Opgegooid bij een databasefout tijdens het verwijderen van een boek."""
    pass

class BoekDeleteOngeldigeParameterException(BoekDeleteException):
    """Opgegooid als er ongeldige parameters zijn aangeleverd aan de delete-functionaliteit."""
    pass
