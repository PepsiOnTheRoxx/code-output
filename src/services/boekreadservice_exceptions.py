class BoekNotFoundException(Exception):
    """Exception raised when a requested book is not found."""
    pass

class DatabaseReadException(Exception):
    """Exception raised when reading from the database fails."""
    pass
