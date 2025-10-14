
import logging, sys
from .log_formatter import JsonFormatter
_cfg=False
def configure_root(level=logging.INFO):
    global _cfg
    if _cfg: return
    h=logging.StreamHandler(sys.stdout); h.setFormatter(JsonFormatter())
    r=logging.getLogger(); r.setLevel(level); r.addHandler(h); _cfg=True
