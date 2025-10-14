# Audit trail hook; safe no-op without a DB sink configured.
def record(action, who=None, details=None):
    _ = (action, who, details)
    return True
