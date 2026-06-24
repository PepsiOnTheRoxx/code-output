class GebruikerDeleteException(Exception):
    """Basisexception voor fouten bij het verwijderen van een gebruiker."""
    pass

class GebruikerNietGevondenException(GebruikerDeleteException):
    """Opgeworpen wanneer de te verwijderen gebruiker niet gevonden wordt."""
    pass

class GebruikerDeleteNietToegestaanException(GebruikerDeleteException):
    """Opgeworpen wanneer verwijderen van gebruiker niet is toegestaan."""
    pass

class GebruikerDeleteDatabaseFoutException(GebruikerDeleteException):
    """Opgeworpen wanneer er een databasefout optreedt bij het verwijderen van de gebruiker."""
    pass

class GebruikerDeleteOnverwachteFoutException(GebruikerDeleteException):
    """Opgeworpen bij onverwachte fouten tijdens het verwijderen van een gebruiker."""
    pass