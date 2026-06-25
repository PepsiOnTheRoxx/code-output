class BoekAPIException(Exception):
    pass

class BoekAPINotFoundException(BoekAPIException):
    pass

class BoekAPIValidationException(BoekAPIException):
    pass

class BoekAPIConflictException(BoekAPIException):
    pass

class BoekAPIUnauthorizedException(BoekAPIException):
    pass

class BoekAPIInternalException(BoekAPIException):
    pass

# Aliases for compatibility with the API code and tests
BoekNotFoundException = BoekAPINotFoundException
InvalidBoekDataException = BoekAPIValidationException
