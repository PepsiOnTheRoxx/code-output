class VernietigingstaakDeleteException(Exception):
    pass

class VernietigingstaakNotFoundException(VernietigingstaakDeleteException):
    pass

class VernietigingstaakDeletePermissionDeniedException(VernietigingstaakDeleteException):
    pass

class VernietigingstaakDeleteDependencyException(VernietigingstaakDeleteException):
    pass

class VernietigingstaakAlreadyDeletedException(VernietigingstaakDeleteException):
    pass

class VernietigingstaakDeleteValidationException(VernietigingstaakDeleteException):
    pass
