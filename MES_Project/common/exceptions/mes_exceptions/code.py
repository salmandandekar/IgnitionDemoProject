
class MESException(Exception): pass
class ValidationException(MESException): pass
class InfrastructureException(MESException): pass
class RepositoryException(MESException): pass
class AccessDenied(MESException): pass
