
from ....common.messaging.envelope import make
from ....common.messaging import router
from ....common.decorators.tracing import traced
from ....common.utils.timeutil import utc_now_iso
class PlanningService(object):
    @traced()
    def plan(self, orderId, resource="LINE-1"):
        now=utc_now_iso()
        env=make("plan","schedule",{"orderId":orderId,"resource":resource,"start":now,"end":now})
        router.publish("schedule.planned", env)
        return env["data"]
