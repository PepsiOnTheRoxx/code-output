class VTArchivarisRelatieAPIException(Exception):
    pass

class VTArchivarisRelatieAPINotFound(VTArchivarisRelatieAPIException):
    pass

class VTArchivarisRelatieAPIInvalidInput(VTArchivarisRelatieAPIException):
    pass

class VTArchivarisRelatieAPIPermissionDenied(VTArchivarisRelatieAPIException):
    pass

class VTArchivarisRelatieAPIConflict(VTArchivarisRelatieAPIException):
    pass

class VTArchivarisRelatieAPIInternalError(VTArchivarisRelatieAPIException):
    pass
