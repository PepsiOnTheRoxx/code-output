class DatabaseSetupException(Exception):
    """Base exception for DatabaseSetup component."""
    pass

class DatabaseConnectionError(DatabaseSetupException):
    """Raised when the database connection fails."""
    pass

class DatabaseInitializationError(DatabaseSetupException):
    """Raised when initializing the SQLite database fails."""
    pass

class TableCreationError(DatabaseSetupException):
    """Raised when creating the Boek table fails."""
    pass

class AttributeCreationError(DatabaseSetupException):
    """Raised when adding an attribute to the Boek table fails."""
    pass

class BoekMetamodelMismatchError(DatabaseSetupException):
    """Raised when the Boek table does not match the metamodel."""
    pass
