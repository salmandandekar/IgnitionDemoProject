# Runtime selection of messaging backend: 'INTERNAL', 'MQTT', 'KAFKA'
def backend():
    try:
        from system.tag import readBlocking
        # read a project tag e.g., [System]Messaging/Backend
        pass
    except Exception:
        return "INTERNAL"
    return "INTERNAL"
