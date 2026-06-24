class VTProceseigenaarRelatieManagementException(Exception):
    """Basis exceptie voor VTProceseigenaarRelatieManagement feature."""
    pass

class VTProceseigenaarRelatieNotFoundException(VTProceseigenaarRelatieManagementException):
    """Exceptie wanneer de relatie tussen Vernietigingstaak en Proceseigenaar niet gevonden wordt."""
    pass

class VTProceseigenaarRelatieAlreadyExistsException(VTProceseigenaarRelatieManagementException):
    """Exceptie wanneer een relatie al bestaat."""
    pass

class VTProceseigenaarRelatieInvalidDataException(VTProceseigenaarRelatieManagementException):
    """Exceptie wanneer de data voor de relatie onjuist of incompleet is."""
    pass

class VTProceseigenaarRelatiePermissionDeniedException(VTProceseigenaarRelatieManagementException):
    """Exceptie wanneer de gebruiker onvoldoende rechten heeft om de relatie te beheren."""
    pass
