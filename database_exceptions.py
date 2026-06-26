class DatabaseSetupException(Exception):
    """Basis exceptie voor DatabaseSetup component."""
    pass

class DatabaseSetupError(DatabaseSetupException):
    """Algemene fout bij DatabaseSetup."""
    pass

class DatabaseInitialisatieException(DatabaseSetupException):
    """Fout bij initialiseren van de database."""
    pass

class DatabaseTabelAanmakenException(DatabaseSetupException):
    """Fout bij het aanmaken van de Boek tabel."""
    pass

class DatabaseVerbindingException(DatabaseSetupException):
    """Fout bij het maken van een verbinding met de database."""
    pass

class DatabaseAttribuutDefinitieException(DatabaseSetupException):
    """Fout met attributendefinities van de entiteit Boek."""
    pass

class DatabaseMetamodelValidatieException(DatabaseSetupException):
    """Fout tijdens validatie van het metamodel voor de tabel Boek."""
    pass
