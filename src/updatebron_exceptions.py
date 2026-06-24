class UpdateBronException(Exception):
    """Base exception for updatebron feature in BronService."""
    pass

class BronNotFoundException(UpdateBronException):
    """Raised when the specified Bron (ObjectType, ElementID:12) is not found."""
    pass

class InvalidBronAttributeValueException(UpdateBronException):
    """Raised when attribute value is invalid (Attributes, ElementID: 15/16)."""
    pass

class BronAttributeUpdateNotAllowedException(UpdateBronException):
    """Raised when updating a specific attribute (ElementID:15/16) is not allowed."""
    pass

class BronUpdateConflictException(UpdateBronException):
    """Raised when there is a conflict during Bron update."""
    pass

class BronUpdateValidationException(UpdateBronException):
    """Raised when validation fails for Bron update."""
    pass