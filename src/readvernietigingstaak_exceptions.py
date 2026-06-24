class ReadVernietigingstaakException(Exception):
    """Base exception for ReadVernietigingstaak feature."""
    pass

class VernietigingstaakNotFoundException(ReadVernietigingstaakException):
    """Raised when the Vernietigingstaak is not found."""
    pass

class UnauthorizedAccessException(ReadVernietigingstaakException):
    """Raised when access to the Vernietigingstaak is unauthorized."""
    pass

class VernietigingstaakInvalidAttributeException(ReadVernietigingstaakException):
    """Raised when an attribute of the Vernietigingstaak is invalid."""
    pass

class VernietigingstaakStatusReadException(ReadVernietigingstaakException):
    """Raised when the status of Vernietigingstaak cannot be retrieved."""
    pass

class VernietigingstaakAantekeningenReadException(ReadVernietigingstaakException):
    """Raised when the aantekeningen of Vernietigingstaak cannot be retrieved."""
    pass

class VernietigingstaakDatumReadException(ReadVernietigingstaakException):
    """Raised when the datum of Vernietigingstaak cannot be retrieved."""
    pass
