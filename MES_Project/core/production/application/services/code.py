
from ....common.messaging.envelope import make
from ....common.messaging import router
from ....common.utils import ids
from ....common.decorators.tracing import traced
class ProductionService(object):
    @traced()
    def create_order(self, materialId, qty):
        oid=ids.new_id("WO")
        env=make("create","workOrder",{"orderId": oid,"materialId": materialId,"qty": qty})
        router.publish("workorder.created", env)
        return env["data"]
    @traced()
    def start(self, orderId):
        router.publish("workorder.started", make("start","workOrder",{"orderId":orderId}))
    @traced()
    def complete(self, orderId, goodQty):
        router.publish("workorder.completed", make("complete","workOrder",{"orderId":orderId,"goodQty":goodQty}))
