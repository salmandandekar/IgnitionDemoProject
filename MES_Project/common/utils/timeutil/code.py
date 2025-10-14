
import datetime
def utc_now_iso(): return datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z"
