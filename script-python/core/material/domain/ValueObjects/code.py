class MaterialId(object):
    def __init__(self, value):
        if not value:
            raise ValueError("MaterialId required")
        self.value = str(value)

class UoM(object):
    def __init__(self, code):
        if not code:
            raise ValueError("UoM code required")
        self.code = code
