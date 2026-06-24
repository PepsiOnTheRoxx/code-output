class VTBehandelaarRelatieManagementException(Exception):
    pass

class BehandelaarKoppelingBestaatAlException(VTBehandelaarRelatieManagementException):
    pass

class BehandelaarKoppelingNietGevondenException(VTBehandelaarRelatieManagementException):
    pass

class OngeldigeBehandelaarException(VTBehandelaarRelatieManagementException):
    pass

class OngeldigeVernietigingstaakException(VTBehandelaarRelatieManagementException):
    pass

class BehandelaarKoppelingVerwijderenNietToegestaanException(VTBehandelaarRelatieManagementException):
    pass

class BehandelaarKoppelingAanmakenNietToegestaanException(VTBehandelaarRelatieManagementException):
    pass
