class CreateBronException(Exception):
    """Base exception for CreateBron feature in BronService."""
    pass

class BronAlreadyExistsException(CreateBronException):
    """Raised when the Bron already exists."""
    pass

class InvalidBronDataException(CreateBronException):
    """Raised when the provided data for creating a Bron is invalid."""
    pass

class BronCreationFailedException(CreateBronException):
    """Raised when the creation of a new Bron fails for an unknown reason."""
    pass

class MissingRequiredAttributeException(CreateBronException):
    """Raised when a required attribute (e.g., AttributeID: 15 or 16) is missing."""
    pass
