class VernietigingstaakReadException(Exception):
    pass

class VernietigingstaakNotFoundException(VernietigingstaakReadException):
    pass

class VernietigingstaakAccessDeniedException(VernietigingstaakReadException):
    pass

class VernietigingstaakInvalidQueryException(VernietigingstaakReadException):
    pass

class VernietigingstaakServiceUnavailableException(VernietigingstaakReadException):
    pass