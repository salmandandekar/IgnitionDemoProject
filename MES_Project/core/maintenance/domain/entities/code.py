
class MaintenanceWO(object):
    def __init__(self, assetId, reason):
        self.woId=assetId+"-MWO"; self.assetId=assetId; self.reason=reason
