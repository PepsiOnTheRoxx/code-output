class CreateVernietigingstaakException(Exception):
    pass

class OngeldigObjectTypeException(CreateVernietigingstaakException):
    pass

class OntbrekendAttribuutException(CreateVernietigingstaakException):
    pass

class OngeldigeAttribuutWaardeException(CreateVernietigingstaakException):
    pass

class DuplicateVernietigingstaakException(CreateVernietigingstaakException):
    pass