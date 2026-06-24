class BronCreateException(Exception):
    """Base exception for BronCreate feature."""
    pass

class BronCreateInvalidNameException(BronCreateException):
    """Raised when the provided bron naam is invalid."""
    pass

class BronCreateInvalidDescriptionException(BronCreateException):
    """Raised when the provided bron beschrijving is invalid."""
    pass

class BronCreateDuplicateException(BronCreateException):
    """Raised when a bron with the same name already exists."""
    pass

class BronCreateMetamodelException(BronCreateException):
    """Raised when there is an inconsistency with the metamodel."""
    pass

class BronCreateServiceException(BronCreateException):
    """Generic exception for BronService errors."""
    pass
