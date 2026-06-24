class GebruikerCreateException(Exception):
    """Base exception for GebruikerCreate feature."""
    pass

class GebruikerCreateNaamMissingException(GebruikerCreateException):
    """Raised when 'Naam' attribute is missing."""
    pass

class GebruikerCreateEmailadresMissingException(GebruikerCreateException):
    """Raised when 'Emailadres' attribute is missing."""
    pass

class GebruikerCreateInvalidEmailadresException(GebruikerCreateException):
    """Raised when 'Emailadres' attribute is invalid."""
    pass

class GebruikerCreateDuplicateEmailadresException(GebruikerCreateException):
    """Raised when 'Emailadres' already exists."""
    pass

class GebruikerCreateObjectCreationFailedException(GebruikerCreateException):
    """Raised when the gebruiker object could not be created."""
    pass