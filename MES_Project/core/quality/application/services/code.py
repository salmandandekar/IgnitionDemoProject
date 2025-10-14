
from ....common.messaging import router
from ....common.messaging.envelope import make
from ....common.decorators.tracing import traced
class QualityService(object):
    @traced()
    def record_check(self, orderId, passed=True, details=None):
        env=make("complete","qualityCheck",{"orderId":orderId,"passed":passed,"details":details or {}})
        router.publish("quality.check.completed", env); return env["data"]
