class BoekCreateServiceException(Exception):
    """Base exception for BoekCreateService errors."""
    pass

class BoekCreateServiceDatabaseError(BoekCreateServiceException):
    """Exception for database errors in BoekCreateService."""
    pass

class BoekCreateServiceValidationError(BoekCreateServiceException):
    """Exception for validation errors in BoekCreateService."""
    pass

class BoekCreateServiceMissingAttributeError(BoekCreateServiceValidationError):
    """Exception for missing required attribute in BoekCreateService."""
    pass

class BoekCreateServiceDuplicateError(BoekCreateServiceException):
    """Exception for duplicate boek entry in BoekCreateService."""
    pass

class BoekCreateServiceUnexpectedError(BoekCreateServiceException):
    """Exception for unexpected errors in BoekCreateService."""
    pass
