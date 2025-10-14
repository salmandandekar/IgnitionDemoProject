
from ..logging.mes_logger import get_logger
log=get_logger("Router")
class MessageAdapter(object):
    def publish(self, topic, message): raise NotImplementedError
    def subscribe(self, topic, handler): raise NotImplementedError
class InternalBus(MessageAdapter):
    def __init__(self): self._subs={}
    def publish(self, topic, message):
        for h in list(self._subs.get(topic, [])): h(message)
        log.debug("pub", extra={"topic": topic})
    def subscribe(self, topic, handler):
        self._subs.setdefault(topic, []).append(handler)
        log.info("sub", extra={"topic": topic, "handlers": len(self._subs[topic])})
_adapters={"internal": InternalBus()}; _active="internal"
def register_adapter(name, adapter): _adapters[name]=adapter
def use_adapter(name):
    global _active
    if name not in _adapters: raise ValueError("unknown adapter %s"%name)
    _active=name; log.info("using", extra={"adapter": name})
def publish(topic, message): _adapters[_active].publish(topic, message)
def subscribe(topic, handler): _adapters[_active].subscribe(topic, handler)
