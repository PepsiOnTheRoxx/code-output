class VTProceseigenaarRelatieException(Exception):
    """Basisklasse voor alle VTProceseigenaarRelatie exceptions."""
    pass

class ProceseigenaarNietGevondenException(VTProceseigenaarRelatieException):
    """Gebruiker of proceseigenaar niet gevonden."""
    pass

class VernietigingstaakNietGevondenException(VTProceseigenaarRelatieException):
    """Vernietigingstaak niet gevonden."""
    pass

class ProceseigenaarRelatieBestaatAlException(VTProceseigenaarRelatieException):
    """De relatie tussen gebruiker en vernietigingstaak als proceseigenaar bestaat al."""
    pass

class ProceseigenaarRelatieNietGevondenException(VTProceseigenaarRelatieException):
    """De relatie tussen gebruiker en vernietigingstaak als proceseigenaar niet gevonden."""
    pass

class OngeldigeProceseigenaarDataException(VTProceseigenaarRelatieException):
    """Ongeldige of incomplete data opgegeven voor proceseigenaar relatie."""
    pass