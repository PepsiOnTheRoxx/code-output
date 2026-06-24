class CreateVernietigingstaakException(Exception):
    pass

class DuplicateVernietigingstaakException(CreateVernietigingstaakException):
    pass

class InvalidVernietigingstaakDataException(CreateVernietigingstaakException):
    pass

class MissingVernietigingstaakAttributeException(CreateVernietigingstaakException):
    pass
