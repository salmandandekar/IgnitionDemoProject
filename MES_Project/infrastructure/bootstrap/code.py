
from ..common.logging.mes_logger import get_logger
from ..common.messaging import router
from ..adapters.messaging.kafka_adapter import KafkaAdapter
from ..adapters.messaging.mqtt_adapter import MQTTAdapter
from ..adapters.cache.ignite_provider import IgniteCacheProvider
from ..common.cache import cache_provider as cache

from ..core.material.application.services import MaterialAppService
from ..core.warehouse.application.services import InventoryService
from ..core.production.application.services import ProductionService
from ..core.planning.application.services import PlanningService
from ..core.energy.application.services import EnergyService
from ..core.kpi.application.services import KPIService
from ..core.alerts.application.services import AlertsService
from ..core.quality.application.services import QualityService
from ..core.maintenance.application.services import MaintenanceService
from ..core.document_control.application.services import DocumentService
from ..core.digital_twin.application.services import TwinService
from ..core.ai_model_ops.application.services import ModelOpsService

log=get_logger("Bootstrap")

def start(adapter="internal"):
    router.register_adapter("kafka", KafkaAdapter())
    router.register_adapter("mqtt", MQTTAdapter())
    router.use_adapter(adapter)
    cache.use_provider(IgniteCacheProvider())

    inv=InventoryService(); prod=ProductionService(); plan=PlanningService()
    energy=EnergyService(); kpi=KPIService(); alerts=AlertsService()
    qual=QualityService(); maint=MaintenanceService(); docs=DocumentService()
    twin=TwinService(); mops=ModelOpsService()

    def on_material_received(env):
        d=env["data"]; inv.add(d["materialId"], d.get("qty",1))

    def on_workorder_created(env):
        d=env["data"]; inv.reserve(d["materialId"], d["qty"]); plan.plan(d["orderId"], resource="LINE-1")

    def on_schedule_planned(env):
        orderId=env["data"]["orderId"]
        energy.set_baseline_for_order(orderId, expected_kwh=50.0)

    def on_energy_baseline_updated(env):
        kpi.update_metric(site="SITE-A", name="EnergyBaselineCount", value=1)

    def on_inventory_shortage(env):
        alerts.raise_alert("HIGH","Inventory shortage", env["data"])

    def on_quality_failed(env):
        if not env["data"]["passed"]:
            alerts.raise_alert("CRITICAL","Quality check failed", env["data"])
            maint.request(assetId="LINE-1", reason="Quality failure investigation")

    router.subscribe("material.received", on_material_received)
    router.subscribe("workorder.created", on_workorder_created)
    router.subscribe("schedule.planned", on_schedule_planned)
    router.subscribe("energy.baseline.updated", on_energy_baseline_updated)
    router.subscribe("inventory.shortage", on_inventory_shortage)
    router.subscribe("quality.check.completed", on_quality_failed)

    log.info("system-started", extra={"adapter": adapter})
    return {"inventory": inv, "production": prod, "planning": plan, "energy": energy,
            "kpi": kpi, "alerts": alerts, "quality": qual, "maintenance": maint,
            "documents": docs, "twin": twin, "modelops": mops}
