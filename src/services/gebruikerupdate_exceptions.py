class GebruikerUpdateException(Exception):
    """Basisklasse voor GebruikerUpdate exceptions."""
    pass

class GebruikerNietGevondenException(GebruikerUpdateException):
    """De opgegeven gebruiker bestaat niet."""
    pass

class OngeldigeGebruikerDataException(GebruikerUpdateException):
    """De opgegeven gebruikersdata is ongeldig."""
    pass

class GebruikerUpdateNietToegestaanException(GebruikerUpdateException):
    """De gebruiker mag niet worden bijgewerkt."""
    pass

class GebruikerUpdateConflictException(GebruikerUpdateException):
    """Conflict tijdens het bijwerken van de gebruiker."""
    pass

class GebruikerUpdateTechnischeFoutException(GebruikerUpdateException):
    """Interne technische fout tijdens gebruiker update."""
    pass
