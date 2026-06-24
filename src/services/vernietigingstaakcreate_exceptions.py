class VernietigingstaakCreateException(Exception):
    """Base exception for VernietigingstaakCreate feature."""
    pass

class InvalidAantekeningenException(VernietigingstaakCreateException):
    """Raised when aantekeningen are invalid."""
    pass

class InvalidDatumException(VernietigingstaakCreateException):
    """Raised when datum is invalid."""
    pass

class InvalidStatusException(VernietigingstaakCreateException):
    """Raised when status is invalid."""
    pass

class MissingAantekeningenException(VernietigingstaakCreateException):
    """Raised when aantekeningen are missing."""
    pass

class VernietigingstaakCreationFailedException(VernietigingstaakCreateException):
    """Raised when task creation fails."""
    pass
