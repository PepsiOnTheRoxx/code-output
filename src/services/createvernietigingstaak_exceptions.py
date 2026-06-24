class CreateVernietigingstaakException(Exception):
    """Base exception for CreateVernietigingstaak feature."""
    pass

class InvalidAantekeningenException(CreateVernietigingstaakException):
    """Exception raised when Aantekeningen attribute is invalid."""
    pass

class InvalidDatumException(CreateVernietigingstaakException):
    """Exception raised when Datum attribute is invalid."""
    pass

class InvalidStatusException(CreateVernietigingstaakException):
    """Exception raised when Status attribute is invalid."""
    pass

class VernietigingstaakCreationFailedException(CreateVernietigingstaakException):
    """Exception raised when the creation of a Vernietigingstaak fails."""
    pass