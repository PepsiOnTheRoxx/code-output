class GebruikerCreateException(Exception):
    """Base exception for GebruikerCreate feature."""
    pass

class GebruikerCreateNaamMissingException(GebruikerCreateException):
    """Raised when 'Naam' attribute is missing."""
    pass

class GebruikerCreateInvalidEmailadresException(GebruikerCreateException):
    """Raised when 'Emailadres' attribute is invalid."""
    pass

class GebruikerCreateDuplicateEmailadresException(GebruikerCreateException):
    """Raised when 'Emailadres' already exists."""
    pass

# Overige niet gebruikte exceptions mogen blijven, maar zijn niet nodig voor deze tests
