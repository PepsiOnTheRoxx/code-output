class BoekSeederException(Exception):
    """Base exception for BoekSeeder errors."""
    pass

class DatabaseCreationError(BoekSeederException):
    """Raised when the SQLite database cannot be created."""
    pass

class DummyBooksInsertionError(BoekSeederException):
    """Raised when inserting dummy books fails."""
    pass

class DatabaseConnectionError(BoekSeederException):
    """Raised when connecting to the database fails."""
    pass

class InvalidBookDataError(BoekSeederException):
    """Raised when invalid book data is provided."""
    pass
