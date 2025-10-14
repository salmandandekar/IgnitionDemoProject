
class AuditEntry(object):
    def __init__(self, who, action, obj):
        self.who=who; self.action=action; self.obj=obj
