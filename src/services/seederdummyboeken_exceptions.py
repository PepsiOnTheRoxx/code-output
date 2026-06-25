class SeederDummyBoekenException(Exception):
    """Base exception for SeederDummyBoeken feature."""
    pass

class BoekSeederDatabaseError(SeederDummyBoekenException):
    """Raised when a database error occurs during seeding."""
    pass

class BoekSeederAlreadySeededError(SeederDummyBoekenException):
    """Raised when the database already contains the minimum number of boeken."""
    pass

class BoekSeederMetamodelMismatchError(SeederDummyBoekenException):
    """Raised when the metamodel does not match expected structure."""
    pass

class BoekSeederInvalidDummyDataError(SeederDummyBoekenException):
    """Raised when the dummy boek data is invalid."""
    pass

class BoekSeederUnknownError(SeederDummyBoekenException):
    """Raised when an unknown error occurs during seeding."""
    pass