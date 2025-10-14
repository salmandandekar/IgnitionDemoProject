from adapters.messaging.MessageRouter import code as router

def publish(envelope):
    # Route to configured backend; topic is noun for ISA-95
    topic = envelope.get("noun", "event")
    return router.publish(topic, envelope)
