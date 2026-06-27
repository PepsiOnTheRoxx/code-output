class BoekSeederException(Exception):
    """Base exception for BoekSeeder component."""
    pass

class BoekSeederMinimumBoekenException(BoekSeederException):
    """Raised when minder dan het minimum aantal dummy boeken wordt toegevoegd."""
    pass

class BoekSeederBoekServiceNietBeschikbaarException(BoekSeederException):
    """Raised when de BoekService niet beschikbaar is."""
    pass

class BoekSeederDuplicaatIsbnException(BoekSeederException):
    """Raised when een dummy boek een bestaande ISBN bevat."""
    pass

class BoekSeederOngeldigeBoekDataException(BoekSeederException):
    """Raised when de dummy boek data ongeldig is."""
    pass

class BoekSeederToevoegenMisluktException(BoekSeederException):
    """Raised when het toevoegen van een dummy boek faalt."""
    pass