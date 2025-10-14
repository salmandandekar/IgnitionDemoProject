from common.exceptions.MessagingException import code as mex

def publish(topic, payload):
    try:
        # If Kafka client jars available, integrate here.
        # Fallback: simulate success to keep flows functional in default env.
        _ = (topic, payload)
        return True
    except Exception as ex:
        raise mex.MessagingException("Kafka publish failed: %s" % str(ex), code="KAFKA_ERROR")
