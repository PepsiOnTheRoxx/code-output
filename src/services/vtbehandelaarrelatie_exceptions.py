class VTBehandelaarRelatieException(Exception):
    '''Base exception for VTBehandelaarRelatieService errors.'''
    pass

class VTBehandelaarRelatieBestaatAlException(VTBehandelaarRelatieException):
    '''Raised when attempting to create a duplicate BehandelaarRelatie.'''
    pass

class VTBehandelaarRelatieNietGevondenException(VTBehandelaarRelatieException):
    '''Raised when the requested BehandelaarRelatie is not found.'''
    pass

class OngeldigeGebruikerException(VTBehandelaarRelatieException):
    '''Raised when the given gebruiker is invalid/nonexistent.'''
    pass

class OngeldigeVernietigingstaakException(VTBehandelaarRelatieException):
    '''Raised when the given vernietigingstaak is invalid/nonexistent.'''
    pass
