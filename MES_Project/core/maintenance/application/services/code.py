
from ....common.messaging import router
from ....common.messaging.envelope import make
from ....common.decorators.tracing import traced
from ..domain.entities import MaintenanceWO
class MaintenanceService(object):
    @traced()
    def request(self, assetId, reason):
        wo=MaintenanceWO(assetId, reason)
        router.publish("maintenance.requested", make("request","maintenance", wo.__dict__)); return wo
