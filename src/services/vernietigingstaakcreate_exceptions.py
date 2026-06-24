class VernietigingstaakCreateException(Exception):
    """Base exception for VernietigingstaakCreate feature."""
    pass

class VernietigingstaakCreateValidationException(VernietigingstaakCreateException):
    """Raised when validation of input data fails for VernietigingstaakCreate."""
    pass

class VernietigingstaakCreateObjectTypeNotFoundException(VernietigingstaakCreateException):
    """Raised when the specified ObjectType (ElementID: 10) is not found."""
    pass

class VernietigingstaakCreateMissingAttributeException(VernietigingstaakCreateException):
    """Raised when a required attribute (ElementID: 10, 11, 12) is missing."""
    pass

class VernietigingstaakCreatePersistenceException(VernietigingstaakCreateException):
    """Raised when creation of Vernietigingstaak fails due to storage or DB errors."""
    pass