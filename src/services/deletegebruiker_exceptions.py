class DeleteGebruikerException(Exception):
    """Base exception for DeleteGebruiker feature."""
    pass

class GebruikerNietGevondenException(DeleteGebruikerException):
    """Exception raised when the gebruiker to delete is not found."""
    pass

class DeleteNietToegestaanException(DeleteGebruikerException):
    """Exception raised when deleting the gebruiker is not allowed."""
    pass

class OnbekendeDeleteFoutException(DeleteGebruikerException):
    """Exception raised for unknown errors during verwijderen van gebruiker."""
    pass