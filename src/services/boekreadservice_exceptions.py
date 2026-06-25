class BoekReadServiceError(Exception):
    """Base exception for BoekReadService errors."""
    pass

class BoekNotFoundError(BoekReadServiceError):
    """Exception raised when a requested book is not found."""
    pass

class BoekDatabaseConnectionError(BoekReadServiceError):
    """Exception raised when database connection fails."""
    pass

class BoekDatabaseReadError(BoekReadServiceError):
    """Exception raised when reading from the database fails."""
    pass

class OngeldigBoekIDError(BoekReadServiceError):
    """Exception raised when an invalid boek ID is provided."""
    pass