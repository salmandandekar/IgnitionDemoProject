class Result(object):
    def __init__(self, ok, value=None, error=None):
        self.ok = ok
        self.value = value
        self.error = error

    @staticmethod
    def Ok(value=None):
        return Result(True, value=value)

    @staticmethod
    def Err(error):
        return Result(False, error=error)
