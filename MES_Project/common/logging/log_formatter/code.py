
import logging, json, time
from ..decorators.tracing import get_correlation_id
class JsonFormatter(logging.Formatter):
    def format(self, record):
        d={"ts": int(time.time()*1000), "lvl": record.levelname, "logger": record.name, "msg": record.getMessage()}
        for k in ("cid","func","ms","tenant","site","user"):
            if hasattr(record, k): d[k]=getattr(record,k)
        d.setdefault("cid", get_correlation_id())
        if record.exc_info: d["exc"]=self.formatException(record.exc_info)
        return json.dumps(d)
