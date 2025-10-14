
from ....common.messaging import router
from ....common.messaging.envelope import make
from ....common.decorators.tracing import traced
from ..domain.entities import Document
class DocumentService(object):
    @traced()
    def release(self, docId, version):
        d=Document(docId, version)
        router.publish("document.released", make("release","document", d.__dict__)); return d
