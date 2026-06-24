class CreateBronException(Exception):
    """Base exception for CreateBron feature in BronService."""
    pass

class BronNaamMissingException(CreateBronException):
    """Raised when 'Naam' attribute is missing during Bron creation."""
    pass

class BronBeschrijvingMissingException(CreateBronException):
    """Raised when 'Beschrijving' attribute is missing during Bron creation."""
    pass

class BronAlreadyExistsException(CreateBronException):
    """Raised when trying to create a Bron that already exists."""
    pass

class BronInvalidDataException(CreateBronException):
    """Raised when provided data for Bron creation is invalid."""
    pass