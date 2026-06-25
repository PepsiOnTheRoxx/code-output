class BoekCreateException(Exception):
    pass

class BoekCreateDatabaseException(BoekCreateException):
    pass

class BoekCreateMissingAttributeException(BoekCreateException):
    pass

class BoekCreateInvalidAuteurException(BoekCreateException):
    pass

class BoekCreateInvalidBeschrijvingException(BoekCreateException):
    pass

class BoekCreateInvalidIsbnException(BoekCreateException):
    pass

class BoekCreateInvalidPublicatiedatumException(BoekCreateException):
    pass

class BoekCreateInvalidKaftFotoUrlException(BoekCreateException):
    pass

class BoekCreateInvalidIsUitgeleendException(BoekCreateException):
    pass

class BoekCreateInvalidUitgeleendDatumException(BoekCreateException):
    pass

class BoekCreateInvalidUitgeleendMaxTotException(BoekCreateException):
    pass
