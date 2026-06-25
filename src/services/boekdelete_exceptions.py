class BoekDeleteException(Exception):
    """Basisklasse voor uitzonderingen in BoekDelete-feature."""
    pass

class BoekNietGevondenException(BoekDeleteException):
    """Boek met opgegeven ID niet gevonden."""
    pass

class BoekDeleteDatabaseException(BoekDeleteException):
    """Fout bij verwijderen van boek uit de database."""
    pass

class BoekVerwijderenNietToegestaanException(BoekDeleteException):
    """Verwijderen van dit boek is niet toegestaan."""
    pass