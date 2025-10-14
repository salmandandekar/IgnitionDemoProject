
from ....common.messaging.envelope import make
from ....common.messaging import router
from ....common.utils import ids
from ....common.decorators.tracing import traced
class MaterialAppService(object):
    @traced()
    def receive(self, name, qty=1, uom="EA"):
        mid=ids.new_id("MAT")
        env=make("receive","material",{"materialId": mid,"name": name,"qty": qty,"uom": uom})
        router.publish("material.received", env)
        return env["data"]
