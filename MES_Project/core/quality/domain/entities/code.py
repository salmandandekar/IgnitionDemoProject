
class QualityCheck(object):
    def __init__(self, orderId, passed, details=None):
        self.orderId=orderId; self.passed=passed; self.details=details or {}
