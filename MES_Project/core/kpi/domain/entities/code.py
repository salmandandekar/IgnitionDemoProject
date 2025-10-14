
from ....common.utils.timeutil import utc_now_iso
class KPIEntry(object):
    def __init__(self, name, value, ts=None):
        self.name=name; self.value=value; self.ts=ts or utc_now_iso()
