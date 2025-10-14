# ISA-95 envelope helpers
import datetime, uuid

def new_envelope(verb, noun, data, source="MES_Project", target="External", version="1.0"):
    return {
        "correlationId": "%s-%s" % (noun, str(uuid.uuid4())),
        "timestamp": datetime.datetime.utcnow().replace(microsecond=0).isoformat()+"Z",
        "verb": verb,
        "noun": noun,
        "data": data,
        "source": source,
        "target": target,
        "version": version
    }
