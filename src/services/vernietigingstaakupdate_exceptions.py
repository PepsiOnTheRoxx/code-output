class VernietigingstaakUpdateException(Exception):
    """Base exception for VernietigingstaakUpdate feature."""
    pass

class VernietigingstaakNietGevondenException(VernietigingstaakUpdateException):
    """Exception thrown when the Vernietigingstaak is not found."""
    pass

class OngeldigeVernietigingstaakDataException(VernietigingstaakUpdateException):
    """Exception thrown when invalid data is provided for updating the Vernietigingstaak."""
    pass

class VernietigingstaakWijzigingNietToegestaanException(VernietigingstaakUpdateException):
    """Exception thrown when the update of Vernietigingstaak is not allowed."""
    pass

class VernietigingstaakServiceFoutException(VernietigingstaakUpdateException):
    """Exception thrown for generic service errors within VernietigingstaakService."""
    pass