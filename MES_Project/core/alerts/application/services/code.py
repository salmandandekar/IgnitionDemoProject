
from ....common.messaging import router
from ....common.messaging.envelope import make
from ....common.decorators.tracing import traced
class AlertsService(object):
    @traced()
    def raise_alert(self, level, message, ctx=None):
        env=make("raise","alert",{"level":level,"message":message,"ctx":ctx or {}})
        router.publish("alert.raised", env); return env["data"]
