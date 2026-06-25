class DatabaseSetupException(Exception):
    """Basisexceptie voor alle DatabaseSetup gerelateerde fouten."""
    pass

class DatabaseInitializationError(DatabaseSetupException):
    """Fout bij initialiseren van de database (bibliotheek.db)."""
    pass

class TableCreationError(DatabaseSetupException):
    """Fout bij het aanmaken van de Boek tabel."""
    pass

class MissingAttributeError(DatabaseSetupException):
    """Fout: verplicht attribuut ontbreekt in de Boek tabel."""
    pass

class InvalidAttributeTypeError(DatabaseSetupException):
    """Fout: onjuist datatype gevonden voor attribuut in de Boek tabel."""
    pass

class DatabaseConnectionError(DatabaseSetupException):
    """Fout bij het maken van connectie met de database."""
    pass

class MetadataMismatchError(DatabaseSetupException):
    """Onverwachte verschillen tussen het datamodel en de database."""
    pass