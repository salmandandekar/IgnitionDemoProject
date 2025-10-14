# Domain service example (e.g., business rules across aggregates)
def validate_creation(name, code):
    if len(name) < 2:
        raise ValueError("Name too short")
    if len(code) < 2:
        raise ValueError("Code too short")
    return True
