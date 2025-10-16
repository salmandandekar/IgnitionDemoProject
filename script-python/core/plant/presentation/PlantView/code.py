"""Presentation layer helpers for plant bounded context."""

import csv
import json
from io import StringIO

from common.logging.LogFactory import code as LogFactory
from core.plant.presentation.PlantController import code as controller_module

_LOG = LogFactory.get_logger("PlantView")

EQUIPMENT_COLUMNS = [
    "ID",
    "Name",
    "Description",
    "AlternateName",
    "Code",
    "EquipmentParentID",
    "parentname",
    "EquipmentType",
    "ReasonTree",
    "HasChildren",
    "DepartmentID",
    "EquipmentNumber",
    "Equipment",
    "FunctionalLocation",
    "ReasonGroups",
    "SetPoint",
    "Teams",
]

EQUIPMENT_DROPDOWN_COLUMNS = [
    "label",
    "value",
    "EquipmentType",
    "DepartmentID",
    "FunctionalLocation",
    "EquipmentNumber",
    "Code",
]

DEPARTMENT_COLUMNS = [
    "DepartmentID",
    "DepartmentName",
    "DepartmentParentID",
    "DepartmentType",
    "JobOrderCompletionThreshold",
    "AlternateName",
    "DepartmentNumber",
    "SortOrder",
    "Department",
    "IsFirst",
    "IsLast",
    "IsOrderLinkingSupported",
    "FunctionalLocation",
    "WorkstationOptimization",
]

DROPDOWN_COLUMNS = ["label", "value"]


def _object_to_dict(obj):
    if hasattr(obj, "to_record"):
        return obj.to_record()
    if isinstance(obj, dict):
        return dict(obj)
    return dict(getattr(obj, "__dict__", {}))


def _to_dataset(records, columns):
    rows = []
    for rec in records:
        rows.append([rec.get(col) for col in columns])
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


def _resolve_username(user_id):
    try:
        from View.FMV import UserView

        return UserView.get_userid_from_username(user_id)
    except Exception:
        return user_id


def get_plant_model(user_id):
    controller = controller_module.PlantController(user_id)
    equipment = controller.get_equipment_tree() or []
    records = [_object_to_dict(item) for item in equipment]
    return _to_dataset(records, EQUIPMENT_COLUMNS)


def get_plant_model_dropdown(user_id):
    controller = controller_module.PlantController(user_id)
    equipment = controller.get_equipment_dropdown() or []
    records = [_object_to_dict(item) for item in equipment]
    return _to_dataset(records, EQUIPMENT_DROPDOWN_COLUMNS)


def insert_equipment(user_id, **kwargs):
    username = _resolve_username(user_id)
    payload = dict(kwargs)
    payload.setdefault("InsertedBy", username)
    payload.setdefault("UpdatedBy", username)
    controller = controller_module.PlantController(user_id)
    result = controller.create_equipment(payload)
    return getattr(result, "value", result)


def insert_machine(user_id, **kwargs):
    return insert_equipment(user_id, **kwargs)


def delete_equipment(user_id, ID):
    controller = controller_module.PlantController(user_id)
    result = controller.delete_equipment(ID)
    return getattr(result, "value", result)


def delete_department(user_id, DepartmentID):
    username = _resolve_username(user_id)
    controller = controller_module.PlantController(user_id)
    result = controller.delete_department(DepartmentID, username)
    return getattr(result, "value", result)


def update_equipment(user_id, **kwargs):
    username = _resolve_username(user_id)
    payload = dict(kwargs)
    payload.setdefault("UpdatedBy", username)
    controller = controller_module.PlantController(user_id)
    result = controller.update_equipment(payload)
    return getattr(result, "value", result)


def update_machine(user_id, **kwargs):
    return update_equipment(user_id, **kwargs)


def update_department(user_id, **kwargs):
    username = _resolve_username(user_id)
    payload = dict(kwargs)
    payload.setdefault("UpdatedBy", username)
    controller = controller_module.PlantController(user_id)
    result = controller.update_department(payload)
    return getattr(result, "value", result)


def insert_department(user_id, **kwargs):
    username = _resolve_username(user_id)
    payload = dict(kwargs)
    payload.setdefault("InsertedBy", username)
    controller = controller_module.PlantController(user_id)
    result = controller.create_department(payload)
    return getattr(result, "value", result)


def get_department(user_id, department_id=None):
    controller = controller_module.PlantController(user_id)
    departments = controller.get_departments(department_id) or []
    records = [_object_to_dict(item) for item in departments]
    return _to_dataset(records, DEPARTMENT_COLUMNS)


def get_department_based_onLineID(user_id, DepartmentID):
    return get_department(user_id, DepartmentID)


def get_equipment(user_id, EquipmentID=None, WorkStationID=None, WorkCenterID=None):
    controller = controller_module.PlantController(user_id)
    return controller.get_equipment_details(EquipmentID, WorkStationID, WorkCenterID)


def get_equipmentid(user_id, EquipmentID=None, WorkStationID=None, WorkCenterID=None):
    response = get_equipment(user_id, EquipmentID, WorkStationID, WorkCenterID)
    headers = ["value", "label", "Code", "FunctionalLocation"]
    data = []
    for row in response or []:
        rec = _object_to_dict(row)
        data.append(
            [
                rec.get("EquipmentID"),
                rec.get("Machine") or rec.get("Equipment"),
                rec.get("Code"),
                rec.get("FunctionalLocation"),
            ]
        )
    try:
        from system.dataset import toDataSet

        return toDataSet(headers, data)
    except Exception:
        return {"headers": headers, "rows": data}


def get_line_workstation_dropdown(user_id, DepartmentID=None):
    controller = controller_module.PlantController(user_id)
    departments = controller.get_department_dropdown(DepartmentID) or []
    records = [_object_to_dict(item) for item in departments]
    return _to_dataset(records, [
        "DepartmentID",
        "DepartmentName",
        "DepartmentParentID",
        "DepartmentTypeID",
        "DepartmentNumber",
        "label",
        "value",
    ])


def get_workcenter_dropdown(user_id):
    controller = controller_module.PlantController(user_id)
    equipment = controller.get_workcenter_dropdown() or []
    records = [_object_to_dict(item) for item in equipment]
    return _to_dataset(records, [
        "ID",
        "Name",
        "Description",
        "AlternateName",
        "Code",
        "EquipmentParentID",
        "parentname",
        "DepartmentID",
        "EquipmentType",
        "label",
        "value",
    ])


def get_equipment_class_dropdown(user_id):
    controller = controller_module.PlantController(user_id)
    classes = controller.get_equipment_class_dropdown() or []
    records = [_object_to_dict(item) for item in classes]
    return _to_dataset(records, [
        "ID",
        "Name",
        "Description",
        "AlternateName",
        "Code",
        "label",
        "value",
    ])


def insert_equipment_class(user_id, **kwargs):
    username = _resolve_username(user_id)
    payload = dict(kwargs)
    payload.setdefault("InsertedBy", username)
    controller = controller_module.PlantController(user_id)
    result = controller.insert_equipment_class(payload)
    return getattr(result, "value", result)


def check_special_char(input_string):
    special_characters = "}~!@#$%^&*(`)+={[]|\\:;<,>.?/\"'"
    if input_string is None:
        return False
    return any(c in special_characters for c in str(input_string))


def get_plant_model_equipment_name(user_id, PlantModelType):
    controller = controller_module.PlantController(user_id)
    return controller.get_equipment_name(PlantModelType)


def update_ws_sequence(user_id, sequence, selected_seq_number, data):
    if selected_seq_number in (None, 0):
        return False

    temp_oproute = list(data or [])
    seq_index = selected_seq_number - 1

    if sequence == "Up":
        if selected_seq_number == 1:
            return False
        index = next(
            (i for i, item in enumerate(temp_oproute) if item.get("SortOrder") == selected_seq_number),
            None,
        )
        if index is None or index == 0:
            return False
        temp_oproute[index]["SortOrder"] = selected_seq_number - 1
        temp_oproute[index - 1]["SortOrder"] = selected_seq_number
    else:
        if selected_seq_number == len(temp_oproute):
            return False
        index = next(
            (i for i, item in enumerate(temp_oproute) if item.get("SortOrder") == selected_seq_number),
            None,
        )
        if index is None or index == len(temp_oproute) - 1:
            return False
        temp_oproute[index]["SortOrder"] = selected_seq_number + 1
        temp_oproute[index + 1]["SortOrder"] = selected_seq_number

    controller = controller_module.PlantController(user_id)
    result = controller.update_workstation_sort_order(temp_oproute)
    return getattr(result, "value", result)


def get_equipment_dropdown(user_id, EquipmentID=None, WorkStationID=None, WorkCenterID=None):
    controller = controller_module.PlantController(user_id)
    equipment = controller.get_machine_dropdown(EquipmentID, WorkStationID, WorkCenterID) or []
    records = [_object_to_dict(item) for item in equipment]
    return _to_dataset(records, DROPDOWN_COLUMNS)


def get_workstation_from_machine(user_id, EquipmentID):
    controller = controller_module.PlantController(user_id)
    return controller.get_workstation_from_machine(EquipmentID)


def export_machines(user_id, EquipmentID=None, WorkStationID=None, WorkCenterID=None):
    controller = controller_module.PlantController(user_id)
    export_data = controller.export_machines(EquipmentID, WorkStationID, WorkCenterID)
    headers = export_data.get("headers", [])
    rows = export_data.get("rows", [])
    try:
        from system.dataset import toDataSet

        return toDataSet(headers, rows)
    except Exception:
        return export_data


def read_and_process_machines_csv(user_id, filedata):
    reader = list(csv.DictReader(StringIO(filedata)))
    duplicate_machines = set()
    for i in range(len(reader) - 1):
        left_name = (reader[i].get("MachineName") or "").strip()
        if not left_name:
            continue
        for j in range(i + 1, len(reader)):
            right_name = (reader[j].get("MachineName") or "").strip()
            if left_name and left_name == right_name:
                duplicate_machines.add(left_name)

    controller = controller_module.PlantController(user_id)
    existing = controller.get_equipment_details(None, None, None) or []

    processed = []
    for row in reader:
        row = {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        row.setdefault("Flag", 0)
        row.setdefault("Reasons", {"value": "", "style": {}})
        errors = []

        if not row.get("MachineName"):
            errors.append("Please Enter Machine Name!!")
        if not row.get("MachineDescription"):
            errors.append("Please Enter Machine Description!!")
        if not row.get("MachineClass"):
            errors.append("Please Enter Machine Class!!")
        if not row.get("WorkCenter"):
            errors.append("Please Enter Work Center!!")
        if not row.get("WorkStation"):
            errors.append("Please Enter Work Station!!")

        if len(row.get("MachineName", "")) > 100:
            errors.append("Machine Name cannot exceed 100 character length !!")
        if len(row.get("MachineDescription", "")) > 200:
            errors.append("Machine description cannot exceed 200 character length !!")
        if row.get("AssetNumber") and len(row.get("AssetNumber")) > 100:
            errors.append("Asset Number cannot exceed 100 character length !!")
        if row.get("EquipmentNumber") and len(row.get("EquipmentNumber")) > 50:
            errors.append("Equipment Number cannot exceed 50 character length !!")

        if check_special_char(row.get("MachineName")) or check_special_char(row.get("FunctionalLocation")):
            errors.append(
                "Machine Name and Functional Location are allowed to have only these special characters Hypen (-), Space ( ), Underscore ( _ )"
            )

        if row.get("MachineName") in duplicate_machines:
            errors.append("Same Machine Name present multiple times")

        action = row.get("Action", "I")
        if action not in ("I", "U", "D"):
            errors.append("Please Enter Valid Action(I/U/D)")

        if action == "I":
            for machine in existing:
                rec = _object_to_dict(machine)
                if rec.get("EquipmentNumber") == row.get("EquipmentNumber") and (
                    rec.get("WorkCenter") != row.get("WorkCenter")
                ):
                    errors.append("Equipment Number already assigned to different Work Center")
                    break

        row_errors = ",".join(errors)
        if errors:
            row["Flag"] = 1
            row["Reasons"] = {
                "value": row_errors,
                "style": {
                    "backgroundColor": "#FF474C",
                    "font-weight": "bold",
                    "color": "#FFFFFF",
                },
            }
        processed.append(row)
    return processed


def filter_machines(machines_data):
    machines_data = machines_data or []
    return [row for row in machines_data if row.get("Flag") == 0]


def bulk_upload_machines(user_id, json_machines, clock_id):
    controller = controller_module.PlantController(user_id)
    result = controller.bulk_upload_machines(json_machines, clock_id)
    return getattr(result, "value", result)
