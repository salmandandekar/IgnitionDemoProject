
"""Domain-specific exception hierarchy for the MES demo project."""


class MESException(Exception):
    """Base class for all custom exceptions raised by the project."""


class ValidationException(MESException):
    """Raised when inputs fail domain validation rules."""


class InfrastructureException(MESException):
    """Raised when infrastructure dependencies cannot be reached or configured."""


class RepositoryException(MESException):
    """Raised when persistence layers experience recoverable errors."""


class AccessDenied(MESException):
    """Raised when the caller lacks the required permissions."""
