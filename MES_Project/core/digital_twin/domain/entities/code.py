
class TwinState(object):
    def __init__(self, assetId, params):
        self.assetId=assetId; self.params=dict(params or {})
