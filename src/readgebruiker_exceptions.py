class ReadGebruikerException(Exception):
    """Base exception for ReadGebruiker feature."""
    pass

class GebruikerNietGevondenException(ReadGebruikerException):
    """De gebruiker kon niet worden gevonden."""
    pass

class OnvoldoendeRechtenReadGebruikerException(ReadGebruikerException):
    """Er zijn onvoldoende rechten om de gebruiker in te zien."""
    pass

class OngeldigeGebruikerIDException(ReadGebruikerException):
    """De opgegeven gebruiker ID is ongeldig."""
    pass

class OnverwachteReadGebruikerException(ReadGebruikerException):
    """Een onverwachte fout is opgetreden bij het inzien van de gebruiker."""
    pass
