from common.exceptions.MessagingException import code as mex

def publish(topic, payload):
    try:
        # Example if Cirrus Link MQTT modules installed:
        # system.cirruslink.engine.publish("myEngine", topic, json.dumps(payload), 0, False)
        # To keep functional without module, we just return True (simulated publish)
        _ = (topic, payload)
        return True
    except Exception as ex:
        raise mex.MessagingException("MQTT publish failed: %s" % str(ex), code="MQTT_ERROR")
