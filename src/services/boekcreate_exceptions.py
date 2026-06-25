class BoekCreateException(Exception):
    """Basisklasse voor uitzonderingen in BoekCreate-feature."""
    pass

class BoekCreateInvalidAttributeException(BoekCreateException):
    """Onjuist attribuutwaarde of ontbrekend verplicht attribuut bij aanmaken boek."""
    pass

class BoekCreateDuplicateException(BoekCreateException):
    """Boek bestaat reeds (duplicaat)."""
    pass

class BoekCreateDatabaseException(BoekCreateException):
    """Fout bij database-operatie tijdens boek aanmaken."""
    pass

class BoekCreateMetamodelMismatchException(BoekCreateException):
    """Mismatch met vereiste metamodel attributen."""
    pass
