class CreateBronException(Exception):
    """Base exception for CreateBron feature."""
    pass

class InvalidBronNameException(CreateBronException):
    """Raised when the provided Bron name is invalid."""
    pass

class InvalidBronDescriptionException(CreateBronException):
    """Raised when the provided Bron description is invalid."""
    pass

class BronAlreadyExistsException(CreateBronException):
    """Raised when trying to create a Bron that already exists."""
    pass

class BronObjectTypeNotFoundException(CreateBronException):
    """Raised when the required ObjectType (ElementID: 12) is not found."""
    pass

class BronNameAttributeNotFoundException(CreateBronException):
    """Raised when the required Attribute for name (ElementID: 15) is not found."""
    pass

class BronDescriptionAttributeNotFoundException(CreateBronException):
    """Raised when the required Attribute for description (ElementID: 16) is not found."""
    pass