class BoekCreateException(Exception):
    pass

class BoekCreateInvalidDataException(BoekCreateException):
    pass

class BoekCreateDatabaseException(BoekCreateException):
    pass

class BoekCreateMissingAttributeException(BoekCreateException):
    pass

class BoekCreateInvalidAuteurException(BoekCreateInvalidDataException):
    pass

class BoekCreateInvalidBeschrijvingException(BoekCreateInvalidDataException):
    pass

class BoekCreateInvalidIsbnException(BoekCreateInvalidDataException):
    pass

class BoekCreateInvalidPublicatiedatumException(BoekCreateInvalidDataException):
    pass

class BoekCreateInvalidKaftFotoUrlException(BoekCreateInvalidDataException):
    pass

class BoekCreateInvalidIsUitgeleendException(BoekCreateInvalidDataException):
    pass

class BoekCreateInvalidUitgeleendDatumException(BoekCreateInvalidDataException):
    pass

class BoekCreateInvalidUitgeleendMaxTotException(BoekCreateInvalidDataException):
    pass