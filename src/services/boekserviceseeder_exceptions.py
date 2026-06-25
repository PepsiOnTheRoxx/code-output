class BoekServiceSeederException(Exception):
    """Base exception for BoekServiceSeeder related errors."""
    pass

class BoekServiceSeederDatabaseError(BoekServiceSeederException):
    """Raised when a database error occurs in BoekServiceSeeder."""
    pass

class BoekServiceSeederInitializationError(BoekServiceSeederException):
    """Raised when BoekServiceSeeder fails during initialization."""
    pass

class BoekServiceSeederDummyBoekenError(BoekServiceSeederException):
    """Raised when dummy books cannot be created or inserted."""
    pass

class BoekServiceSeederTableCreationError(BoekServiceSeederException):
    """Raised when the Boek table cannot be created."""
    pass

class BoekServiceSeederAlreadySeededError(BoekServiceSeederException):
    """Raised when seeding is attempted but the table is already seeded."""
    pass