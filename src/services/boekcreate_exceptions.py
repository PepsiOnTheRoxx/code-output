class BoekCreateException(Exception):
    """Base exception for BoekCreate feature in BoekService."""
    pass

class BoekCreateInvalidDataException(BoekCreateException):
    """Raised when invalid data is provided for creating a Boek."""
    pass

class BoekCreateMissingAttributeException(BoekCreateException):
    """Raised when a required attribute is missing for creating a Boek."""
    pass

class BoekCreateInvalidISBNException(BoekCreateException):
    """Raised when the provided ISBN is invalid."""
    pass

class BoekCreateDuplicateISBNException(BoekCreateException):
    """Raised when a Boek with the same ISBN already exists."""
    pass

class BoekCreateInvalidPublicatiedatumException(BoekCreateException):
    """Raised when the publicatiedatum is invalid or in the future."""
    pass

class BoekCreateInvalidUitgeleendDatumException(BoekCreateException):
    """Raised when the uitgeleend_datum is invalid or inconsistent."""
    pass

class BoekCreateInvalidKaftFotoURLException(BoekCreateException):
    """Raised when the provided kaft_foto_url is not a valid URL."""
    pass

class BoekCreateDatabaseException(BoekCreateException):
    """Raised when the database layer fails during Boek creation."""
    pass