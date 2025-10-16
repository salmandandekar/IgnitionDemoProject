"""Domain value objects for the Material bounded context."""

class MaterialId(object):
    """Type safe identifier that tolerates transient entities without IDs."""

    def __init__(self, value=None):
        if value in (None, ""):
            self.value = None
        else:
            self.value = str(value)

    def __str__(self):
        return self.value or ""

    def __repr__(self):
        return "MaterialId(%r)" % self.value

    def __eq__(self, other):
        if isinstance(other, MaterialId):
            return self.value == other.value
        return self.value == other

    def __hash__(self):
        return hash(self.value)

    def exists(self):
        return self.value is not None


class RouteId(object):
    def __init__(self, value=None):
        if value in (None, ""):
            self.value = None
        else:
            self.value = str(value)

    def __str__(self):
        return self.value or ""

    def exists(self):
        return self.value is not None


class CycleTime(object):
    def __init__(self, minutes=None):
        if minutes in (None, "", False):
            self.minutes = None
            return
        try:
            minutes = float(minutes)
        except Exception:
            raise ValueError("Cycle time must be numeric")
        if minutes < 0:
            raise ValueError("Cycle time cannot be negative")
        self.minutes = minutes

    def as_minutes(self):
        return self.minutes

    def __float__(self):
        return float(self.minutes or 0.0)

    def __repr__(self):
        return "CycleTime(%s)" % self.minutes


class BaseQuantity(object):
    def __init__(self, value=None):
        if value in (None, ""):
            raise ValueError("Base quantity is required")
        try:
            qty = float(value)
        except Exception:
            raise ValueError("Base quantity must be numeric")
        if qty <= 0:
            raise ValueError("Base quantity must be greater than 0")
        self.value = qty

    def as_float(self):
        return float(self.value)

    def __float__(self):
        return float(self.value)

    def __repr__(self):
        return "BaseQuantity(%s)" % self.value


class JsonTag(object):
    def __init__(self, value=None):
        self.value = value or {}

    def __repr__(self):
        return "JsonTag(%r)" % self.value
