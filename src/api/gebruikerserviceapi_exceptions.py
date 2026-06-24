class GebruikerAPIException(Exception):
    """Basisklasse voor uitzonderingen in GebruikerAPI."""
    pass

class GebruikerNietGevondenException(GebruikerAPIException):
    """Exception indien gebruiker niet gevonden wordt."""
    pass

class OngeldigeGebruikerDataException(GebruikerAPIException):
    """Exception indien gebruikersdata ongeldig is."""
    pass

class GebruikerAanmakenMisluktException(GebruikerAPIException):
    """Exception indien het aanmaken van een gebruiker mislukt."""
    pass

class GebruikerBijwerkenMisluktException(GebruikerAPIException):
    """Exception indien het bijwerken van gebruiker mislukt."""
    pass

class GebruikerVerwijderenMisluktException(GebruikerAPIException):
    """Exception indien het verwijderen van een gebruiker mislukt."""
    pass

class OngeautoriseerdToegangGebruikerException(GebruikerAPIException):
    """Exception indien ongeautoriseerd toegang wordt gepoogd."""
    pass
