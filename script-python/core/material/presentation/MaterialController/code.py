from common.decorators.TraceDecorator import code as tracedec
from common.decorators.ExceptionHandlerDecorator import code as exdec
from common.security.AccessControl import code as access
from common.context.SessionContext import code as session
from core.material.application.Commands import code as cmds
from core.material.application.CommandHandlers import code as ch
from core.material.application.Queries import code as q
from core.material.application.QueryHandlers import code as qh
from core.material.infrastructure.RepositoryAdapter import code as repo
from core.material.infrastructure.MessagingAdapter import code as msg

@tracedec.traced
@exdec.guarded
@access.require(["MES-Author"])
def create(material_id, name, code):
    c = cmds.CreateMaterial(material_id, name, code)
    return ch.handle_create(c, repository=_Repo(), messenger=_Msg())

@tracedec.traced
@exdec.guarded
def get(material_id):
    return qh.handle_get_by_id(q.GetMaterialById(material_id), repository=_Repo())

# Adapter wrappers to conform to handler expectations
class _Repo(object):
    def save(self, material, tx=None): return repo.save(material, tx=tx)
    def get_by_id(self, material_id): return repo.get_by_id(material_id)

class _Msg(object):
    def publish(self, envelope): return msg.publish(envelope)
