
from ....common.cache import cache_provider as cache
from ....common.messaging import router
from ....common.messaging.envelope import make
from ....common.logging.mes_logger import get_logger
from ..domain.entities import KPIEntry
log=get_logger("KPIService")
class KPIService(object):
    def __init__(self, region="kpi"): self.region=region
    def update_metric(self, site, name, value):
        e=KPIEntry(name, value)
        cache.set(self.region, "%s:%s"%(name, site), e.__dict__)
        router.publish("kpi.updated", make("update","kpi",{"site":site,"name":name,"value":value}))
        return e
