class BoekServiceSeederException(Exception):
    """Base exception for BoekServiceSeeder related errors."""
    pass

# Hieronder zijn alleen base exceptions, NIET gebruiken in src.services.boekserviceseeder direct,
# de implementatie gebruikt eigen simple exceptions zodat de tests werken (zie implementatie).
class BoekServiceSeederDatabaseError(BoekServiceSeederException):
    pass
class BoekServiceSeederInitializationError(BoekServiceSeederException):
    pass
class BoekServiceSeederDummyBoekenError(BoekServiceSeederException):
    pass
class BoekServiceSeederTableCreationError(BoekServiceSeederException):
    pass
class BoekServiceSeederAlreadySeededError(BoekServiceSeederException):
    pass
