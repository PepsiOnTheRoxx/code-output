class DatabaseSetupException(Exception):
    """Basis exceptie voor DatabaseSetup component."""
    pass

class DatabaseConnectionError(DatabaseSetupException):
    """Kan geen verbinding maken met de database."""
    pass

class DatabaseTableCreationError(DatabaseSetupException):
    """Fout bij het aanmaken van een of meer tabellen."""
    pass

class AttributeMissingError(DatabaseSetupException):
    """Verplicht attribuut ontbreekt in metamodel of database."""
    pass

class AttributeTypeError(DatabaseSetupException):
    """Attribuut heeft een ongeldig type volgens het metamodel."""
    pass

class BoekTableMissingError(DatabaseSetupException):
    """Tabel 'Boek' ontbreekt in database."""
    pass

class BoekColumnMissingError(DatabaseSetupException):
    """Kolom van 'Boek' ontbreekt in database."""
    pass

class BoekInvalidColumnTypeError(DatabaseSetupException):
    """'Boek'-kolomtype komt niet overeen met definitie in metamodel."""
    pass

class DatabaseMigrationRequired(DatabaseSetupException):
    """Database migratie vereist vanwege gewijzigde metamodel structuur."""
    pass