class BoekSeederException(Exception):
    """Base exception for BoekSeeder component."""
    pass

class BoekSeederInvalidBookCountException(BoekSeederException):
    """Raised when trying to seed less than the minimum required books."""
    pass

class BoekSeederServiceException(BoekSeederException):
    """Raised when there is a problem communicating with the BoekService."""
    pass

class BoekSeederDuplicateBookException(BoekSeederException):
    """Raised when attempting to seed duplicate books."""
    pass

class BoekSeederInvalidBoekDataException(BoekSeederException):
    """Raised when one or more Boek objects have invalid data."""
    pass