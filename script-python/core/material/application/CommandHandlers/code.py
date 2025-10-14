from common.decorators.TraceDecorator import code as tracedec
from common.decorators.ExceptionHandlerDecorator import code as exdec
from common.decorators.TransactionDecorator import code as txdec
from common.decorators.CacheDecorator import code as cdec
from infrastructure.DatabaseConfig import code as dbc
from core.material.domain.Entities import code as entities
from core.material.domain.DomainServices import code as dsvc
from core.material.domain.Events import code as events
from core.material.ports.RepositoryPort import code as repo_port
from core.material.ports.MessagingPort import code as msg_port
from infrastructure.ISA95Config import code as isa95

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
