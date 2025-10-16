"""Command handlers orchestrating write operations for the plant bounded context."""

import json

from common.decorators.ExceptionHandlerDecorator import code as exception_decorator
from common.decorators.TraceDecorator import code as trace_decorator
from common.utils.Result import code as result_module

Result = result_module.Result


@exception_decorator.guarded
@trace_decorator.traced
def handle_create_equipment(command, repository):
    record = command.equipment.to_record()
    result = repository.insert_equipment(record, command.user_id)
    return Result.Ok(result)


@exception_decorator.guarded
@trace_decorator.traced
def handle_update_equipment(command, repository):
    record = command.equipment.to_record()
    result = repository.update_equipment(record, command.user_id)
    return Result.Ok(result)


@exception_decorator.guarded
@trace_decorator.traced
def handle_delete_equipment(command, repository):
    result = repository.delete_equipment(command.equipment_id, command.user_id)
    return Result.Ok(result)


@exception_decorator.guarded
@trace_decorator.traced
def handle_create_department(command, repository):
    record = command.department.to_record()
    result = repository.insert_department(record, command.user_id)
    return Result.Ok(result)


@exception_decorator.guarded
@trace_decorator.traced
def handle_update_department(command, repository):
    record = command.department.to_record()
    result = repository.update_department(record, command.user_id)
    return Result.Ok(result)


@exception_decorator.guarded
@trace_decorator.traced
def handle_delete_department(command, repository):
    result = repository.delete_department(command.department_id, command.updated_by, command.user_id)
    return Result.Ok(result)


@exception_decorator.guarded
@trace_decorator.traced
def handle_insert_equipment_class(command, repository):
    record = command.equipment_class.to_record()
    result = repository.insert_equipment_class(record, command.user_id)
    return Result.Ok(result)


@exception_decorator.guarded
@trace_decorator.traced
def handle_update_workstation_sort_order(command, repository):
    payload = [item.to_record() for item in command.sort_orders]
    result = repository.update_workstation_sort_order(json.dumps(payload), command.user_id)
    return Result.Ok(result)


@exception_decorator.guarded
@trace_decorator.traced
def handle_bulk_upload_machines(command, repository):
    result = repository.bulk_upload_machines(command.json_payload, command.clock_id, command.user_id)
    return Result.Ok(result)
