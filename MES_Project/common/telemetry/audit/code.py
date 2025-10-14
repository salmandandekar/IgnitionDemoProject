
from ..logging.mes_logger import get_logger
from ..utils.timeutil import utc_now_iso
log=get_logger("Audit")
def record(event_type, data, cid=None):
    log.info("audit", extra={"event_type": event_type, "cid": cid})
    return {"type": event_type, "data": data, "ts": utc_now_iso()}
