class DatabaseSetupException(Exception):
    """Algemene fout tijdens DatabaseSetup."""
    pass

class DatabaseConnectionException(DatabaseSetupException):
    """Fout bij het verbinden met de SQLite database."""
    pass

class DatabaseInitializationException(DatabaseSetupException):
    """Fout bij het initialiseren van de database."""
    pass

class TableCreationException(DatabaseSetupException):
    """Fout bij het aanmaken van de 'Boek' tabel."""
    pass

class MissingAttributeException(DatabaseSetupException):
    """Een vereist attribuut ontbreekt in het metamodel."""
    pass

class AttributeTypeMismatchException(DatabaseSetupException):
    """Een attribuut heeft een onjuiste of incompatibele datatypedefinitie."""
    pass

class InvalidDateFormatException(DatabaseSetupException):
    """Een datumattribuut heeft een ongeldig formaat."""
    pass

class DuplicateTableException(DatabaseSetupException):
    """De 'Boek' tabel bestaat al in de database."""
    pass

class DatabaseFileAccessException(DatabaseSetupException):
    """Fout bij toegang tot het databasebestand."""
    pass