class CreateGebruikerException(Exception):
    """Base exception for CreateGebruiker feature."""
    pass

class GebruikerNaamLeegException(CreateGebruikerException):
    """Exception raised when the naam attribute is empty."""
    pass

class GebruikerEmailLeegException(CreateGebruikerException):
    """Exception raised when the email attribute is empty."""
    pass

class GebruikerEmailOngeldigException(CreateGebruikerException):
    """Exception raised when the email is not a valid email address."""
    pass

class GebruikerBestaatAlException(CreateGebruikerException):
    """Exception raised when a gebruiker with same naam and/or email already exists."""
    pass

class GebruikerAanmakenMisluktException(CreateGebruikerException):
    """Exception raised when creating a gebruiker fails for an unspecified reason."""
    pass