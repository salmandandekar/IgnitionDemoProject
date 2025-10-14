class MaterialCachePort(object):
    def get(self, key): raise Exception("Override")
    def put(self, key, value): raise Exception("Override")
    def invalidate(self, key=None): raise Exception("Override")
