
from ..utils.timeutil import utc_now_iso
from ..utils import ids
def make(verb, noun, data, correlation_id=None, attributes=None):
    return {"correlationId": correlation_id or ids.new_id("corr"), "timestamp": utc_now_iso(),
            "verb": verb, "noun": noun, "data": data, "attributes": attributes or {}}
