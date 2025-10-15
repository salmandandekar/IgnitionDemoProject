from common.decorators import TraceDecorator as tracedec
from common.decorators import ExceptionHandlerDecorator as exdec
from common.decorators import TransactionDecorator as txdec
from common.decorators import CacheDecorator as cdec
from infrastructure import DatabaseConfig as dbc
from core.material.domain import Entities as entities
from core.material.domain import DomainServices as dsvc
from core.material.domain import Events as events
from core.material.ports import RepositoryPort as repo_port
from core.material.ports import MessagingPort as msg_port
from infrastructure import ISA95Config as isa95

# Cache key function for handlers
def _mat_key(cmd): 
    return "material:%s" % cmd.id

@tracedec.traced
@exdec.guarded
@txdec.transactional(datasource=dbc.datasource_name())
def handle_create(cmd, repository, messenger, _tx=None):
    assert isinstance(repository, repo_port.MaterialRepositoryPort)
    assert isinstance(messenger, msg_port.MaterialMessagingPort)
    dsvc.validate_creation(cmd.name, cmd.code)
    m = entities.Material(cmd.id, cmd.name, cmd.code)
    repository.save(m, tx=_tx)
    # publish domain event as ISA-95 envelope
    envelope = isa95.new_envelope("report", "materialEvent", {"materialId": cmd.id, "name": cmd.name, "code": cmd.code})
    messenger.publish(envelope)
    # invalidate cache if needed (fresh read-through on next query)
    return m
