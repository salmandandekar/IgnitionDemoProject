
from ....common.cache import cache_provider as cache
from ....common.messaging import router
from ....common.messaging.envelope import make
from ....common.decorators.tracing import traced
from ..domain.entities import EnergyBaseline
REGION="energy"
class EnergyService(object):
    @traced()
    def set_baseline_for_order(self, orderId, expected_kwh):
        eb=EnergyBaseline(orderId, expected_kwh)
        cache.set(REGION, "baseline:"+orderId, {"orderId":orderId, "expected_kwh": expected_kwh})
        router.publish("energy.baseline.updated", make("update","energyBaseline", eb.__dict__))
        return eb
