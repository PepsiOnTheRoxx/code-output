class DatabaseSetupError(Exception):
    """Algemene fout in DatabaseSetup component."""
    pass

class DatabaseConnectionError(DatabaseSetupError):
    """Fout bij het verbinden met de SQLite database."""
    pass

class DatabaseInitializationError(DatabaseSetupError):
    """Fout bij het initialiseren van de database structuur."""
    pass

class TableCreationError(DatabaseSetupError):
    """Fout bij het aanmaken van de Boek tabel."""
    pass

class AttributeMappingError(DatabaseSetupError):
    """Fout bij het mappen van attributen uit het metamodel."""
    pass

class InvalidMetamodelError(DatabaseSetupError):
    """Metamodel data voor DatabaseSetup is ongeldig of incompleet."""
    pass
