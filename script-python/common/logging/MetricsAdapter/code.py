# Hook for pushing metrics to Prometheus/Influx; safe no-op if not configured.
def increment(metric_name, labels=None):
    _ = (metric_name, labels)
    # integrate with your metrics stack if available.
    return True
