class GebruikerCreateException(Exception):
    """Basisexception voor GebruikerCreate-gerelateerde fouten."""
    pass

class GebruikerAlreadyExistsException(GebruikerCreateException):
    """Gebruiker bestaat al."""
    pass

class InvalidGebruikerDataException(GebruikerCreateException):
    """Gebruikersdata is ongeldig."""
    pass

class MissingRequiredAttributeException(GebruikerCreateException):
    """Verplicht attribuut ontbreekt."""
    pass

class GebruikerServiceInternalError(GebruikerCreateException):
    """Interne fout in GebruikerService tijdens creatie."""
    pass

class StorageException(GebruikerCreateException):
    """Exception voor opslagfouten."""
    pass
