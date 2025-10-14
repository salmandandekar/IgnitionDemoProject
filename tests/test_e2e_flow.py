
import sys, os
PROJ=os.path.join(os.path.dirname(__file__), "..", "MES_Project")
sys.path.insert(0, PROJ)
from MES_Project.infrastructure.bootstrap.code import start
from MES_Project.core.material.application.services import MaterialAppService
from MES_Project.core.production.application.services import ProductionService
from MES_Project.common.cache import cache_provider as cache
def test_full_flow():
    services=start(adapter="internal")
    mat=MaterialAppService().receive("Widget-X", qty=100)
    wo=services["production"].create_order(materialId=mat["materialId"], qty=100)
    eb=cache.get("energy","baseline:"+wo["orderId"])
    assert eb is not None and eb["expected_kwh"]>0
    kpi=cache.get("kpi","EnergyBaselineCount:SITE-A")
    assert kpi is not None and kpi["value"]>=1
    print("OK")
if __name__=="__main__":
    test_full_flow()
