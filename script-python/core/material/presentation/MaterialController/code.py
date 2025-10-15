from common.decorators import TraceDecorator as tracedec
from common.decorators import ExceptionHandlerDecorator as exdec
from common.security import AccessControl as access
from common.context import SessionContext as session
from core.material.application import Commands as cmds
from core.material.application import CommandHandlers as ch
from core.material.application import Queries as q
from core.material.application import QueryHandlers as qh
from core.material.infrastructure import RepositoryAdapter as repo
from core.material.infrastructure import MessagingAdapter as msg

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
