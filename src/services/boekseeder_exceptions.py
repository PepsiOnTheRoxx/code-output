class BoekSeederException(Exception):
    """Base exception for BoekSeeder errors."""
    pass

class OnvoldoendeBoekenException(BoekSeederException):
    """Raised when less than the minimum required dummy books are provided."""
    pass

class BoekSeederServiceException(BoekSeederException):
    """Raised when an error occurs in the service layer of BoekSeeder."""
    pass

class OngeldigBoekTypeException(BoekSeederException):
    """Raised when an invalid type is used for Boek."""
    pass