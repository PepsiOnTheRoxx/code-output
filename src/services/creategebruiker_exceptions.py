class CreateGebruikerException(Exception):
    """Base exception for CreateGebruiker feature in GebruikerService."""
    pass

class GebruikerAlreadyExistsException(CreateGebruikerException):
    """Raised when attempting to create a user that already exists."""
    pass

class InvalidGebruikerDataException(CreateGebruikerException):
    """Raised when provided data for creating a user is invalid."""
    pass

class MissingGebruikerAttributeException(CreateGebruikerException):
    """Raised when a required attribute is missing during user creation."""
    pass

class ObjectTypeNotFoundException(CreateGebruikerException):
    """Raised when the required ObjectType (ElementID: 11) is not found."""
    pass

class Attribute13ValidationException(CreateGebruikerException):
    """Raised when validation for Attribute (ElementID: 13) fails."""
    pass

class Attribute14ValidationException(CreateGebruikerException):
    """Raised when validation for Attribute (ElementID: 14) fails."""
    pass