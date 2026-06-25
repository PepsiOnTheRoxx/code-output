class BoekSeederException(Exception):
    """Basisklasse voor BoekSeeder exceptions."""
    pass

class BoekSeederDatabaseError(BoekSeederException):
    """Exception voor database fouten tijdens seeden."""
    pass

class BoekSeederMinimumBooksError(BoekSeederException):
    """Exception als het minimum aantal boeken niet gehaald wordt."""
    pass

class BoekSeederInvalidBoekDataError(BoekSeederException):
    """Exception voor ongeldig Boek data tijdens seeden."""
    pass

class BoekSeederAlreadySeededError(BoekSeederException):
    """Exception als er reeds gesedeerd is."""
    pass