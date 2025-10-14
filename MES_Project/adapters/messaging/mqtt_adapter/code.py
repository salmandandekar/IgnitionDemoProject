
from ...common.messaging.router import MessageAdapter
from ...common.logging.mes_logger import get_logger
log=get_logger("MQTTAdapter")
class MQTTAdapter(MessageAdapter):
    def __init__(self): self._topics={}
    def publish(self, topic, message):
        for h in self._topics.get(topic, []): h(message)
        log.info("publish", extra={"topic": topic})
    def subscribe(self, topic, handler):
        self._topics.setdefault(topic, []).append(handler)
        log.info("subscribe", extra={"topic": topic})
