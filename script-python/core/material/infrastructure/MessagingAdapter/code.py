from adapters.messaging import MessageRouter as router

def publish(envelope):
    # Route to configured backend; topic is noun for ISA-95
    topic = envelope.get("noun", "event")
    return router.publish(topic, envelope)
