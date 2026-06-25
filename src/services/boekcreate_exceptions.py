class BoekCreateException(Exception):
    """Base exception for BoekCreate feature in BoekService."""
    pass

class BoekCreateValidationException(BoekCreateException):
    """Raised when book data validation fails."""
    pass

class BoekCreateDatabaseException(BoekCreateException):
    """Raised when book creation fails due to database errors."""
    pass

# REMOVE this duplicate/unused exception to prevent confusion.
# class BoekCreateDuplicateException(BoekCreateException):
#     pass
# class BoekCreatePermissionException(BoekCreateException):
#     pass
