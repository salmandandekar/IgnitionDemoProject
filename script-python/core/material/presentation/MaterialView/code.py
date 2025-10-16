"""Facade functions used by Perspective views for material workflows."""

import csv
import io

from core.material.presentation.MaterialController import code as MaterialControllerModule

try:
    string_types = (basestring,)  # type: ignore[name-defined]
except Exception:  # pragma: no cover - Python 3 fallback
    string_types = (str,)

DEFAULT_MATERIAL_COLUMNS = [
    "ID",
    "MaterialName",
    "Description",
    "MaterialDescription",
    "NCM",
    "BaseQuantity",
    "IdealCycleTime",
    "TargetCycleTime",
    "HourlyTarget",
    "Category",
    "MaterialGroupID",
    "DefaultRoute",
    "NCMTypeID",
]

DEFAULT_ROUTE_LINK_COLUMNS = [
    "RouteID",
    "RouteName",
    "Description",
    "MaterialID",
    "Status",
    "IsDefault",
    "RouteNumber",
    "Revision",
    "IsSecondary",
]

DEFAULT_ROUTE_COLUMNS = [
    "RouteID",
    "RouteName",
    "Description",
    "Status",
    "label",
    "value",
]


def _object_to_dict(obj):
    if hasattr(obj, "to_record"):
        record = obj.to_record()
    elif isinstance(obj, dict):
        record = dict(obj)
    else:
        record = dict(getattr(obj, "__dict__", {}))
    if "Name" in record and "MaterialName" not in record:
        record["MaterialName"] = record.get("Name")
    if "ID" not in record and "MaterialID" in record:
        record["ID"] = record["MaterialID"]
    return record


def _to_dataset(records, columns):
    rows = []
    for rec in records:
        row = [rec.get(col) for col in columns]
        rows.append(row)
    try:
        from system.dataset import toDataSet

        return toDataSet(columns, rows)
    except Exception:
        return {"headers": columns, "rows": rows}


def _dataset_to_dicts(dataset):
    if dataset is None:
        return []
    if isinstance(dataset, list):
        return [dict(item) if isinstance(item, dict) else item for item in dataset]
    rows = []
    try:
        row_count = dataset.getRowCount()
        columns = list(dataset.getColumnNames())
        for i in range(row_count):
            row = {}
            for col in columns:
                try:
                    row[col] = dataset.getValueAt(i, col)
                except Exception:
                    row[col] = dataset.getValueAt(i, columns.index(col))
            rows.append(row)
    except Exception:
        try:
            rows.append(dict(dataset))
        except Exception:
            pass
    return rows


def get_materialData(user_id):
    controller = MaterialControllerModule.MaterialController(user_id)
    materials = controller.get_materials() or []
    records = [_object_to_dict(m) for m in materials]
    return _to_dataset(records, DEFAULT_MATERIAL_COLUMNS)


def get_MaterialRouteLink(user_id, material_id):
    controller = MaterialControllerModule.MaterialController(user_id)
    route_links = controller.get_material_route_links(material_id) or []
    records = [_object_to_dict(r) for r in route_links]
    return _to_dataset(records, DEFAULT_ROUTE_LINK_COLUMNS)


def get_routeList(user_id):
    controller = MaterialControllerModule.MaterialController(user_id)
    routes = controller.get_routes() or []
    records = [_object_to_dict(r) for r in routes]
    dataset = _to_dataset(records, DEFAULT_ROUTE_COLUMNS)
    filtered = [row for row in _dataset_to_dicts(dataset) if row.get("Status") == "Approved"]
    return filtered


def insert_materialRouteLink(user_id, route_dataset, material_id):
    controller = MaterialControllerModule.MaterialController(user_id)
    return controller.insert_material_route_link(route_dataset, material_id)


def update_default_route(user_id, material_id, route_id, is_secondary=0):
    controller = MaterialControllerModule.MaterialController(user_id)
    return controller.update_default_route(material_id, route_id, is_secondary)


def delete_materialroute_link(user_id, material_id, route_id):
    controller = MaterialControllerModule.MaterialController(user_id)
    return controller.delete_material_route_link(material_id, route_id)


def insert_material(user_id, sap_materialid, material_name, material_desc, idle_cycle_time, updated_by, ncm_type_id, base_quant):
    payload = {
        "Name": sap_materialid,
        "MaterialName": sap_materialid,
        "Description": material_name,
        "MaterialDescription": material_desc,
        "IdealCycleTime": idle_cycle_time,
        "UpdatedBy": updated_by,
        "NCMTypeID": ncm_type_id,
        "BaseQuantity": base_quant,
        "Category": 1,
        "SortOrder": 1,
        "StatusID": 1,
        "MaterialGroupID": 1,
        "UnitofMeasureID": 1,
        "UnitofMeasure1ID": 1,
        "IsDeleted": 0,
    }
    controller = MaterialControllerModule.MaterialController(user_id)
    return controller.create_material(payload)


def update_material(user_id, material_id, sap_materialid, material_name, material_desc, idle_cycle_time, updated_by, ncm_type_id, base_quant):
    payload = {
        "ID": material_id,
        "Name": sap_materialid,
        "MaterialName": sap_materialid,
        "Description": material_name,
        "MaterialDescription": material_desc,
        "IdealCycleTime": idle_cycle_time,
        "UpdatedBy": updated_by,
        "NCMTypeID": ncm_type_id,
        "BaseQuantity": base_quant,
        "Category": 1,
        "SortOrder": 1,
        "StatusID": 1,
        "MaterialGroupID": 1,
        "UnitofMeasureID": 1,
        "UnitofMeasure1ID": 1,
        "IsDeleted": 0,
    }
    controller = MaterialControllerModule.MaterialController(user_id)
    return controller.update_material(payload)


def delete_material(user_id, material_id, updated_by):
    controller = MaterialControllerModule.MaterialController(user_id)
    return controller.delete_material(material_id, updated_by)


def get_ncm_types(user_id):
    controller = MaterialControllerModule.MaterialController(user_id)
    ncm_types = controller.get_ncm_types() or []
    return [getattr(n, "to_choice", lambda: _object_to_dict(n))() for n in ncm_types]


def bulk_upload_materials(user_id, json_materials, clock_id):
    controller = MaterialControllerModule.MaterialController(user_id)
    return controller.bulk_upload_materials(json_materials, clock_id)


def export_materials(user_id):
    controller = MaterialControllerModule.MaterialController(user_id)
    export_payload = controller.export_materials()
    headers = export_payload.get("headers", [])
    data = export_payload.get("data", [])
    try:
        from system.dataset import toDataSet

        return toDataSet(headers, data)
    except Exception:
        return {"headers": headers, "rows": data}


def read_and_process_materials_csv(user_id, filedata):
    if isinstance(filedata, bytes):
        filedata = filedata.decode("utf-8")
    reader = csv.DictReader(io.StringIO(filedata))
    rows = []
    for raw in reader:
        row = dict(raw)
        for key in list(row.keys()):
            if isinstance(row[key], string_types):
                row[key] = row[key].strip()
        row.setdefault("IdealCycleTime", row.get("IdleCycleTime(min)", "0"))
        row.setdefault("BaseQuantity", row.get("BaseQuantity", "0"))
        rows.append(row)

    controller = MaterialControllerModule.MaterialController(user_id)
    materials = controller.get_materials() or []
    routes = controller.get_routes() or []
    ncm_types = controller.get_ncm_types() or []

    try:
        from View.FMV import WorkOrderView

        workorders = WorkOrderView.get_sap_order_ids(user_id)
    except Exception:
        workorders = []

    processed = controller.validate_bulk_material_rows(
        rows,
        existing_materials=[_object_to_dict(m) for m in materials],
        ncm_types=[getattr(n, "to_choice", lambda: _object_to_dict(n))() for n in ncm_types],
        routes=[_object_to_dict(r) for r in routes],
        work_orders=_dataset_to_dicts(workorders),
    )
    return processed


def filter_materials(materials_data):
    return [row for row in materials_data if row.get("Flag") == 0]
