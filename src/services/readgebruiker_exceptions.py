class ReadGebruikerException(Exception):
    """Base exception for ReadGebruiker feature in GebruikerService."""
    pass

class GebruikerNotFoundException(ReadGebruikerException):
    """Exception raised when the requested gebruiker is not found."""
    pass

class GebruikerAccessDeniedException(ReadGebruikerException):
    """Exception raised when access to the gebruiker is denied."""
    pass

class GebruikerInvalidInputException(ReadGebruikerException):
    """Exception raised when input for gebruiker retrieval is invalid."""
    pass

class GebruikerServiceUnavailableException(ReadGebruikerException):
    """Exception raised when the GebruikerService is unavailable."""
    pass