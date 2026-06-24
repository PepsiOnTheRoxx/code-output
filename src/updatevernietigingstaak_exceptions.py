class UpdateVernietigingstaakException(Exception):
    """Base exception for UpdateVernietigingstaak feature."""
    pass

class VernietigingstaakNotFoundException(UpdateVernietigingstaakException):
    """Raised when the specified Vernietigingstaak does not exist."""
    pass

class InvalidVernietigingstaakDataException(UpdateVernietigingstaakException):
    """Raised when provided data for Vernietigingstaak is invalid."""
    pass

class AttributeUpdateNotAllowedException(UpdateVernietigingstaakException):
    """Raised when an update to a protected Attribute is attempted."""
    pass

class AttributeValueConflictException(UpdateVernietigingstaakException):
    """Raised when there is a conflict in attribute values during the update."""
    pass

class UpdateNotAllowedException(UpdateVernietigingstaakException):
    """Raised when an update is not allowed for the current status."""
    pass
