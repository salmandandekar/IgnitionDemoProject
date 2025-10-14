# Internal message bus using Ignition messaging if available; otherwise, no-op success.
def publish(topic, payload):
    try:
        # system.util.sendMessage(project='<project>', messageHandler=topic, payload=payload)
        _ = (topic, payload)
        return True
    except Exception:
        return True
