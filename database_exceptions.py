class DatabaseSetupException(Exception):
    """Base exception for DatabaseSetup component."""
    pass

class DatabaseInitializationError(DatabaseSetupException):
    """Error occurred during initialization of the database."""
    pass

class TableCreationError(DatabaseSetupException):
    """Error occurred while creating the 'Boek' table."""
    pass

class AttributeCreationError(DatabaseSetupException):
    """Error occurred while creating attributes for 'Boek'."""
    pass

class DatabaseConnectionError(DatabaseSetupException):
    """Error occurred while connecting to the SQLite database."""
    pass

class DatabaseIntegrityError(DatabaseSetupException):
    """Integrity constraint violated during database setup."""
    pass

class DatabaseConfigurationError(DatabaseSetupException):
    """Database configuration is invalid or incomplete."""
    pass