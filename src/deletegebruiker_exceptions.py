class DeleteGebruikerException(Exception):
    """Base exception for DeleteGebruiker feature."""
    pass

class GebruikerNietGevondenException(DeleteGebruikerException):
    """Raised when the specified Gebruiker is not found."""
    pass

class GebruikerVerwijderenNietToegestaanException(DeleteGebruikerException):
    """Raised when deleting the Gebruiker is not permitted."""
    pass

class GebruikerDeleteDatabaseFoutException(DeleteGebruikerException):
    """Raised when a database error occurs during Gebruiker deletion."""
    pass

class OngeldigeGebruikerIDException(DeleteGebruikerException):
    """Raised when an invalid Gebruiker ID is provided for deletion."""
    pass