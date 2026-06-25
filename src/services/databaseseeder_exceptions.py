class DatabaseSeederException(Exception):
    """Base exception for the DatabaseSeeder component."""
    pass

class DatabaseSeederSeedError(DatabaseSeederException):
    """Raised when seeding the database fails."""
    pass

class DatabaseSeederFileNotFoundError(DatabaseSeederException):
    """Raised when a required file for seeding is missing."""
    pass

class DatabaseSeederInvalidBookDataError(DatabaseSeederException):
    """Raised when book data is invalid during seeding."""
    pass

class DatabaseSeederConnectionError(DatabaseSeederException):
    """Raised when the database connection fails during seeding."""
    pass