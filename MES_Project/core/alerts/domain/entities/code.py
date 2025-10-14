
class Alert(object):
    def __init__(self, level, message, ctx=None):
        self.level=level; self.message=message; self.ctx=ctx or {}
