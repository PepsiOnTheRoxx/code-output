class BoekCreateException(Exception):
    """Base exception for BoekCreate feature in BoekService."""
    pass

class BoekCreateValidationException(BoekCreateException):
    """Raised when validation fails during creation of a Boek."""
    pass

class BoekCreateAuteurMissingException(BoekCreateValidationException):
    """Raised when the 'auteur' attribute is missing or invalid."""
    pass

class BoekCreateBeschrijvingMissingException(BoekCreateValidationException):
    """Raised when the 'beschrijving' attribute is missing or invalid."""
    pass

class BoekCreateIsbnMissingException(BoekCreateValidationException):
    """Raised when the 'isbn' attribute is missing or invalid."""
    pass

class BoekCreatePublicatiedatumInvalidException(BoekCreateValidationException):
    """Raised when the 'publicatiedatum' attribute is missing or invalid."""
    pass

class BoekCreateKaftFotoUrlInvalidException(BoekCreateValidationException):
    """Raised when the 'kaft_foto_url' attribute is missing or invalid."""
    pass

class BoekCreateIsUitgeleendInvalidException(BoekCreateValidationException):
    """Raised when the 'is_uitgeleend' attribute is missing or invalid."""
    pass

class BoekCreateUitgeleendDatumInvalidException(BoekCreateValidationException):
    """Raised when the 'uitgeleend_datum' attribute is missing or invalid."""
    pass

class BoekCreateUitgeleendMaxTotInvalidException(BoekCreateValidationException):
    """Raised when the 'uitgeleend_max_tot' attribute is missing or invalid."""
    pass

class BoekCreateDuplicateIsbnException(BoekCreateException):
    """Raised when a Boek with the same ISBN already exists."""
    pass

class BoekCreatePersistenceException(BoekCreateException):
    """Raised when there is an error saving the Boek in the DB."""
    pass