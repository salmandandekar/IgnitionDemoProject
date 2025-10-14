
from ....common.messaging import router
from ....common.messaging.envelope import make
from ....common.decorators.tracing import traced
from ..domain.entities import TwinState
class TwinService(object):
    @traced()
    def update(self, assetId, params):
        ts=TwinState(assetId, params)
        router.publish("twin.updated", make("update","twinState", ts.__dict__)); return ts
