class VTProceseigenaarRelatieException(Exception):
    pass
class ProceseigenaarNietGevondenException(VTProceseigenaarRelatieException):
    pass
class VernietigingstaakNietGevondenException(VTProceseigenaarRelatieException):
    pass
class ProceseigenaarRelatieBestaatAlException(VTProceseigenaarRelatieException):
    pass
class ProceseigenaarRelatieNietGevondenException(VTProceseigenaarRelatieException):
    pass
class OngeldigeProceseigenaarDataException(VTProceseigenaarRelatieException):
    pass
