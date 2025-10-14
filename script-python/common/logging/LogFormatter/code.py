# Simple formatter utilities; keep formatting responsibility here.
def fmt(msg, **kwargs):
    if not kwargs:
        return msg
    parts = [msg] + [("%s=%s" % (k, kwargs[k])) for k in sorted(kwargs.keys())]
    return " | ".join(parts)
