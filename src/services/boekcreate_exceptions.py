class BoekCreateException(Exception):
    pass

class BoekCreateValidationException(BoekCreateException):
    pass

class BoekCreateDatabaseException(BoekCreateException):
    pass

class BoekCreateAlreadyExistsException(BoekCreateException):
    pass

class BoekCreateMissingAttributeException(BoekCreateException):
    def __init__(self, attribute_name):
        self.attribute_name = attribute_name
        super().__init__(f"Missing required attribute: {attribute_name}")

class BoekCreateInvalidAttributeException(BoekCreateException):
    def __init__(self, attribute_name, reason):
        self.attribute_name = attribute_name
        self.reason = reason
        super().__init__(f"Invalid value for attribute '{attribute_name}': {reason}")

class BoekCreatePermissionDeniedException(BoekCreateException):
    pass