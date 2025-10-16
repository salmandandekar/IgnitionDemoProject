"""Query handlers orchestrating read operations for the plant bounded context."""

from common.decorators.ExceptionHandlerDecorator import code as exception_decorator
from common.decorators.TraceDecorator import code as trace_decorator


def _normalize_filters(filters):
    return {k: v for k, v in (filters or {}).items() if v not in (None, "", [])}


@exception_decorator.guarded
@trace_decorator.traced
def handle_get_equipment_tree(query, repository):
    return repository.fetch_equipment_tree(query.user_id)


@exception_decorator.guarded
@trace_decorator.traced
def handle_get_equipment_dropdown(query, repository):
    return repository.fetch_equipment_dropdown(query.user_id)


@exception_decorator.guarded
@trace_decorator.traced
def handle_get_workcenter_dropdown(query, repository):
    return repository.fetch_workcenter_dropdown(query.user_id)


@exception_decorator.guarded
@trace_decorator.traced
def handle_get_machine_dropdown(query, repository):
    return repository.fetch_machine_dropdown(_normalize_filters(query.filters), query.user_id)


@exception_decorator.guarded
@trace_decorator.traced
def handle_get_departments(query, repository):
    return repository.fetch_departments(query.department_id, query.user_id)


@exception_decorator.guarded
@trace_decorator.traced
def handle_get_department_dropdown(query, repository):
    return repository.fetch_department_dropdown(query.department_id, query.user_id)


@exception_decorator.guarded
@trace_decorator.traced
def handle_get_equipment_details(query, repository):
    return repository.fetch_equipment_details(_normalize_filters(query.filters), query.user_id)


@exception_decorator.guarded
@trace_decorator.traced
def handle_get_equipment_class_dropdown(query, repository):
    return repository.fetch_equipment_class_dropdown(query.user_id)


@exception_decorator.guarded
@trace_decorator.traced
def handle_get_equipment_name(query, repository):
    return repository.fetch_equipment_name(query.plant_model_type, query.user_id)


@exception_decorator.guarded
@trace_decorator.traced
def handle_get_workstation_from_machine(query, repository):
    return repository.fetch_workstation_from_machine(query.equipment_id, query.user_id)


@exception_decorator.guarded
@trace_decorator.traced
def handle_export_machines(query, repository):
    records = repository.fetch_equipment_details(_normalize_filters(query.filters), query.user_id)
    headers = [
        "MachineName",
        "MachineDescription",
        "AssetNumber",
        "EquipmentNumber",
        "FunctionalLocation",
        "MachineClass",
        "WorkCenter",
        "WorkStation",
        "Action",
    ]
    rows = []
    for rec in records or []:
        if hasattr(rec, "to_record"):
            rec = rec.to_record()
        rows.append(
            [
                rec.get("Machine") or rec.get("Equipment") or rec.get("Name"),
                rec.get("Description"),
                rec.get("Code"),
                rec.get("EquipmentNumber"),
                rec.get("FunctionalLocation"),
                rec.get("MachineClass"),
                rec.get("WorkCenter"),
                rec.get("WorkStation"),
                "I",
            ]
        )
    return {"headers": headers, "rows": rows}


@exception_decorator.guarded
@trace_decorator.traced
def handle_filter_valid_machines(query):
    return [row for row in query.machines_data or [] if row.get("Flag") == 0]
