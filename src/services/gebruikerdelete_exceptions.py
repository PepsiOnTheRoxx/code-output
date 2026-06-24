class GebruikerDeleteException(Exception):
    """Basisklasse voor GebruikerDelete exceptions."""
    pass

class GebruikerNietGevondenException(GebruikerDeleteException):
    """Gebruiker kon niet worden gevonden."""
    pass

class GebruikerVerwijderFoutException(GebruikerDeleteException):
    """Algemene fout tijdens verwijderen van gebruiker."""
    pass

class OnvoldoendeRechtenException(GebruikerDeleteException):
    """Onvoldoende rechten om gebruiker te verwijderen."""
    pass