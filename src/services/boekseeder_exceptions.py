class BoekSeederException(Exception):
    """Base exception for BoekSeeder component."""
    pass

class BoekSeederDatabaseError(BoekSeederException):
    """Raised when a database error occurs during seeding."""
    pass

class BoekSeederServiceUnavailable(BoekSeederException):
    """Raised when the Boek service is unavailable."""
    pass

class BoekSeederInvalidDataError(BoekSeederException):
    """Raised when invalid data is encountered for Boek records."""
    pass

class BoekSeederInsufficientRecordsError(BoekSeederException):
    """Raised when fewer than the minimum required Boek records are created."""
    pass