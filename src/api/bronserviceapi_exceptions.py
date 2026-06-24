class BronServiceAPIException(Exception):
    """Base exception for BronServiceAPI related errors."""
    pass

class BronNotFoundException(BronServiceAPIException):
    """Exception raised when a requested resource is not found."""
    pass

class BronAlreadyExistsException(BronServiceAPIException):
    """Exception raised when trying to create a resource that already exists."""
    pass
