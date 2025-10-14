
import uuid
def new_id(prefix=None):
    v=str(uuid.uuid4()); return ("%s-%s"%(prefix,v)) if prefix else v
