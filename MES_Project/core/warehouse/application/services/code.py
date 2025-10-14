
from ....common.cache import cache_provider as cache
from ....common.messaging import router
from ....common.messaging.envelope import make
from ....common.decorators.tracing import traced
from ..domain.entities import InventoryItem
REGION="inventory"
class InventoryService(object):
    def __init__(self, default_loc="WH1"): self.default_loc=default_loc
    @traced()
    def add(self, materialId, qty, location=None):
        loc=location or self.default_loc
        key="%s@%s"%(materialId, loc)
        cur=cache.get(REGION, key) or {"materialId": materialId, "qty": 0, "location": loc}
        cur["qty"] += qty; cache.set(REGION, key, cur)
        router.publish("inventory.updated", make("update","inventory",cur))
        return InventoryItem(materialId, cur["qty"], loc)
    @traced()
    def reserve(self, materialId, qty, location=None):
        loc=location or self.default_loc
        key="%s@%s"%(materialId, loc)
        cur=cache.get(REGION, key)
        if not cur or cur["qty"]<qty:
            router.publish("inventory.shortage", make("shortage","inventory",{"materialId":materialId,"qty":qty,"location":loc}))
            return None
        cur["qty"] -= qty; cache.set(REGION, key, cur)
        router.publish("inventory.reserved", make("reserve","inventory",{"materialId":materialId,"qty":qty,"location":loc}))
        return cur
