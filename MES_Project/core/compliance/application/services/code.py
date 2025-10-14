
from ....common.telemetry import audit
from ....common.messaging import router
from ....common.messaging.envelope import make
class ComplianceService(object):
    def audit(self, who, action, obj):
        rec=audit.record("audit", {"who":who,"action":action,"obj":obj})
        router.publish("compliance.audit", make("record","audit", rec)); return rec
