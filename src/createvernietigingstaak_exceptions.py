class CreateVernietigingstaakException(Exception):
    """Base exception for CreateVernietigingstaak feature."""
    pass

class InvalidAantekeningenException(CreateVernietigingstaakException):
    """Raised when aantekeningen are invalid."""
    pass

class MissingAantekeningenException(CreateVernietigingstaakException):
    """Raised when aantekeningen are missing."""
    pass

class InvalidDatumException(CreateVernietigingstaakException):
    """Raised when datum is invalid."""
    pass

class MissingDatumException(CreateVernietigingstaakException):
    """Raised when datum is missing."""
    pass

class InvalidStatusException(CreateVernietigingstaakException):
    """Raised when status is invalid."""
    pass

class ObjectTypeNotFoundException(CreateVernietigingstaakException):
    """Raised when the referenced ObjectType does not exist."""
    pass
