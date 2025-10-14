
from ...common.messaging.router import MessageAdapter
from ...common.logging.mes_logger import get_logger
log=get_logger("KafkaAdapter")
class KafkaAdapter(MessageAdapter):
    def __init__(self): self._bus={}
    def publish(self, topic, message):
        for h in self._bus.get(topic, []): h(message)
        log.info("publish", extra={"topic": topic})
    def subscribe(self, topic, handler):
        self._bus.setdefault(topic, []).append(handler)
        log.info("subscribe", extra={"topic": topic})
