class UpdateGebruikerException(Exception):
    """Basisklasse voor alle UpdateGebruiker exceptions."""


class GebruikerNietGevondenException(UpdateGebruikerException):
    """Gebruiker werd niet gevonden voor update."""


class OngeldigeGebruikerDataException(UpdateGebruikerException):
    """De verstrekte gebruiker data is ongeldig."""


class GebruikerUpdateNietToegestaanException(UpdateGebruikerException):
    """Update van gebruiker is niet toegestaan."""


class AttributeNietBeschikbaarException(UpdateGebruikerException):
    """Een vereist attribuut voor de gebruiker is niet beschikbaar."""


class ObjectTypeNietGeldigException(UpdateGebruikerException):
    """Het ObjectType voor update is niet geldig."""