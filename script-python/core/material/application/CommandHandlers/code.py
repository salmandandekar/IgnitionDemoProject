"""Application service layer for handling write operations."""

from common.utils.Result import code as ResultModule
from core.material.domain.Events import code as events

Result = ResultModule.Result


def _invalidate_material_cache(cache_port, user_id):
    if not cache_port:
        return
    try:
        cache_port.invalidate("materials:%s" % user_id)
    except Exception:
        pass


def handle_create_material(cmd, repository, cache_port=None, messenger=None):
    result = repository.insert_material(cmd.material, cmd.user_id)
    _invalidate_material_cache(cache_port, cmd.user_id)
    if messenger:
        messenger.publish(events.MaterialCreated(cmd.material.material_id.value, cmd.material.name))
        messenger.info("Material created", material=cmd.material.to_record())
    return Result.Ok(result)


def handle_update_material(cmd, repository, cache_port=None, messenger=None):
    result = repository.update_material(cmd.material, cmd.user_id)
    _invalidate_material_cache(cache_port, cmd.user_id)
    if messenger:
        messenger.publish(events.MaterialUpdated(cmd.material.material_id.value, cmd.material.name))
        messenger.info("Material updated", material=cmd.material.to_record())
    return Result.Ok(result)


def handle_delete_material(cmd, repository, cache_port=None, messenger=None):
    result = repository.delete_material(cmd.material_id, cmd.updated_by, cmd.user_id)
    _invalidate_material_cache(cache_port, cmd.user_id)
    if messenger:
        messenger.publish(events.MaterialDeleted(cmd.material_id, cmd.updated_by))
        messenger.info("Material deleted", material_id=cmd.material_id)
    return Result.Ok(result)


def handle_insert_route_link(cmd, repository, messenger=None):
    result = repository.insert_route_link(cmd.route_dataset, cmd.material_id, cmd.user_id)
    if messenger:
        messenger.publish(events.MaterialRoutesLinked(cmd.material_id, [cmd.route_dataset]))
        messenger.info("Material route linked", material_id=cmd.material_id)
    return Result.Ok(result)


def handle_update_default_route(cmd, repository, messenger=None):
    result = repository.update_default_route(cmd.material_id, cmd.route_id, cmd.is_secondary, cmd.user_id)
    if messenger:
        messenger.info(
            "Material default route updated",
            material_id=cmd.material_id,
            route_id=cmd.route_id,
            is_secondary=cmd.is_secondary,
        )
    return Result.Ok(result)


def handle_delete_route_link(cmd, repository, messenger=None):
    result = repository.delete_route_link(cmd.material_id, cmd.route_id, cmd.user_id)
    if messenger:
        messenger.info("Material route link deleted", material_id=cmd.material_id, route_id=cmd.route_id)
    return Result.Ok(result)


def handle_bulk_upload_materials(cmd, repository, messenger=None):
    result = repository.bulk_upload_materials(cmd.json_materials, cmd.clock_id, cmd.user_id)
    if messenger:
        messenger.publish(events.MaterialsBulkImported(result.get("SuccessCount", 0), result.get("FailureCount", 0)))
        messenger.info("Bulk materials upload executed", summary=result)
    return Result.Ok(result)
