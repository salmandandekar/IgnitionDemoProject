# Provide minimal mocks for 'system' APIs used in adapters/decorators
class _DB(object):
    def runPrepQuery(self, sql, params, tx=None):
        return []
    def runPrepUpdate(self, sql, params, tx=None):
        return 1
    def beginTransaction(self, ds): return object()
    def commitTransaction(self, tx): pass
    def rollbackTransaction(self, tx): pass
    def closeTransaction(self, tx): pass

class _Util(object):
    def getLogger(self, name): 
        class L(object):
            def info(self, m): pass
            def warn(self, m): pass
            def error(self, m): pass
            def debug(self, m): pass
        return L()
    def getUserName(self): return "tester"

db = _DB()
util = _Util()
