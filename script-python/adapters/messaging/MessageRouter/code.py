from infrastructure import MessagingConfig as cfg
from adapters.messaging import MQTTAdapter as mqtt
from adapters.messaging import KafkaAdapter as kafka
from adapters.messaging import InternalBusAdapter as internal

def publish(topic, payload):
    b = cfg.backend().upper()
    if b == "MQTT":
        return mqtt.publish(topic, payload)
    elif b == "KAFKA":
        return kafka.publish(topic, payload)
    else:
        return internal.publish(topic, payload)
