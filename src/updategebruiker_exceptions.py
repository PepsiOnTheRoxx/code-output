class UpdateGebruikerException(Exception):
    """Basisklasse voor alle UpdateGebruiker exceptions."""

class GebruikerNietGevondenException(UpdateGebruikerException):
    """Gebruiker werd niet gevonden voor update."""

class OngeldigeGebruikersgegevensException(UpdateGebruikerException):
    """De verstrekte gebruikersgegevens zijn ongeldig."""

class UpdateNietToegestaanException(UpdateGebruikerException):
    """Update van gebruiker is niet toegestaan."""

class AttributeNietBeschikbaarException(UpdateGebruikerException):
    """Een vereist attribuut voor de gebruiker is niet beschikbaar."""

class ObjectTypeNietGeldigException(UpdateGebruikerException):
    """Het ObjectType voor update is niet geldig."""
