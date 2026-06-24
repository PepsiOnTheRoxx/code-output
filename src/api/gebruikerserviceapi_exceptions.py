class GebruikerAPIException(Exception):
    """Base exception for GebruikerAPI errors."""
    pass

class GebruikerNietGevondenException(GebruikerAPIException):
    """Gebruiker niet gevonden."""
    pass

class GebruikerAanmakenMisluktException(GebruikerAPIException):
    """Aanmaken van gebruiker mislukt."""
    pass

class GebruikerBijwerkenMisluktException(GebruikerAPIException):
    """Bijwerken van gebruiker mislukt."""
    pass

class GebruikerVerwijderenMisluktException(GebruikerAPIException):
    """Verwijderen van gebruiker mislukt."""
    pass

class OngeldigeGebruikerDataException(GebruikerAPIException):
    """De meegegeven gebruiker data is ongeldig."""
    pass

class GebruikerAPIAuthorisatieException(GebruikerAPIException):
    """Geen toestemming voor deze operatie."""
    pass