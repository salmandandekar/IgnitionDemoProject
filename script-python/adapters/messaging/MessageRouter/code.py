from infrastructure.MessagingConfig import code as cfg
from adapters.messaging.MQTTAdapter import code as mqtt
from adapters.messaging.KafkaAdapter import code as kafka
from adapters.messaging.InternalBusAdapter import code as internal

def publish(topic, payload):
    b = cfg.backend().upper()
    if b == "MQTT":
        return mqtt.publish(topic, payload)
    elif b == "KAFKA":
        return kafka.publish(topic, payload)
    else:
        return internal.publish(topic, payload)
