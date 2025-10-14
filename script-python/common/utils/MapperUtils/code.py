def to_dict(obj):
    try:
        return dict(obj.__dict__)
    except Exception:
        return {"value": obj}
