class MESException(Exception):
    def __init__(self, message, code="MES_ERROR", data=None, user_message=None):
        super(MESException, self).__init__(message)
        self.message = message
        self.code = code
        self.data = data or {}
        self.user_message = (
            user_message or "An unexpected error occurred. Please contact support."
        )

    def __str__(self):
        return self.user_message
