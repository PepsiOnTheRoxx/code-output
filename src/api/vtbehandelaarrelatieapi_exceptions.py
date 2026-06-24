class VTBehandelaarRelatieAPIException(Exception):
    """Base exception for VTBehandelaarRelatieAPI errors."""
    pass

class VTBehandelaarRelatieNotFoundException(VTBehandelaarRelatieAPIException):
    """Exception raised when a VTBehandelaar-relatie is not found."""
    pass

class VTBehandelaarRelatieAlreadyExistsException(VTBehandelaarRelatieAPIException):
    """Exception raised when a VTBehandelaar-relatie already exists."""
    pass

class VTBehandelaarRelatieValidationException(VTBehandelaarRelatieAPIException):
    """Exception raised for validation errors in VTBehandelaar-relatie input."""
    pass

class VTBehandelaarRelatiePermissionDeniedException(VTBehandelaarRelatieAPIException):
    """Exception raised when permission is denied for VTBehandelaar-relatie actions."""
    pass

class VTBehandelaarRelatieServiceException(VTBehandelaarRelatieAPIException):
    """Exception for internal service errors in VTBehandelaar-relatie operations."""
    pass

# Aliases for test compatibility
ValidationException = VTBehandelaarRelatieValidationException
NotFoundException = VTBehandelaarRelatieNotFoundException
AlreadyExistsException = VTBehandelaarRelatieAlreadyExistsException
PermissionDeniedException = VTBehandelaarRelatiePermissionDeniedException
ServiceException = VTBehandelaarRelatieServiceException
