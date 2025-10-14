class MESException(Exception):
    def __init__(self, message, code="MES_ERROR", data=None):
        super(MESException, self).__init__(message)
        self.code = code
        self.data = data or {}
