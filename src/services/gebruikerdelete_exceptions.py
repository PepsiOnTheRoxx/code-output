class GebruikerDeleteException(Exception):
    """Basisklasse voor GebruikerDelete exceptions."""
    pass

class GebruikerBestaatNietException(GebruikerDeleteException):
    """Gebruiker kon niet worden gevonden."""
    pass

class VerwijderNietToegestaanException(GebruikerDeleteException):
    """Niet toegestaan om gebruiker te verwijderen."""
    pass

class GebruikerNietGevondenException(GebruikerDeleteException):
    """Alias voor backwards compatibility."""
    pass

class GebruikerVerwijderFoutException(GebruikerDeleteException):
    """Algemene fout tijdens verwijderen van gebruiker."""
    pass

class OnvoldoendeRechtenException(GebruikerDeleteException):
    """Onvoldoende rechten om gebruiker te verwijderen."""
    pass
