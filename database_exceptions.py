class DatabaseSetupError(Exception):
    """Raised when setup or connection to the database fails."""
    pass

class DatabaseSetupException(Exception):
    """Base exception for DatabaseSetup component."""
    pass

class DatabaseConnectionError(DatabaseSetupException):
    """Raised when connecting to the database fails."""
    pass

class DatabaseInitializationError(DatabaseSetupException):
    """Raised when database initialization fails."""
    pass

class BoekTableCreationError(DatabaseSetupException):
    """Raised when creation of the Boek table fails."""
    pass

class InvalidBoekAttributeError(DatabaseSetupException):
    """Raised when an invalid attribute is found for Boek."""
    pass
