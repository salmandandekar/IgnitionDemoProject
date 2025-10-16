"""Entities and aggregate roots for the Plant bounded context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def _to_int(value: Any) -> Optional[int]:
    try:
        if value in (None, "", "None"):
            return None
        return int(value)
    except Exception:
        return None


def _to_float(value: Any) -> Optional[float]:
    try:
        if value in (None, "", "None"):
            return None
        return float(value)
    except Exception:
        return None


@dataclass
class Equipment(object):
    equipment_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    alternate_name: Optional[str] = None
    code: Optional[str] = None
    equipment_parent_id: Optional[int] = None
    parent_name: Optional[str] = None
    work_unit_thing_name: Optional[str] = None
    production_count_multiplier: Optional[float] = None
    is_first_unit: Optional[int] = None
    is_last_unit: Optional[int] = None
    equipment_type: Optional[str] = None
    reason_tree: Optional[str] = None
    has_children: Optional[bool] = None
    department_id: Optional[int] = None
    equipment_number: Optional[str] = None
    equipment: Optional[str] = None
    is_order_linking_supported: Optional[bool] = None
    functional_location: Optional[str] = None
    reason_groups: Optional[str] = None
    set_point: Optional[float] = None
    teams: Optional[str] = None

    def to_record(self) -> Dict[str, Any]:
        return {
            "ID": self.equipment_id,
            "Name": self.name,
            "Description": self.description,
            "AlternateName": self.alternate_name,
            "Code": self.code,
            "EquipmentParentID": self.equipment_parent_id,
            "parentname": self.parent_name,
            "WorkUnitThingName": self.work_unit_thing_name,
            "ProductionCountMultiplier": self.production_count_multiplier,
            "IsFirstUnit": self.is_first_unit,
            "IsLastUnit": self.is_last_unit,
            "EquipmentType": self.equipment_type,
            "ReasonTree": self.reason_tree,
            "HasChildren": int(self.has_children) if self.has_children is not None else None,
            "DepartmentID": self.department_id,
            "EquipmentNumber": self.equipment_number,
            "Equipment": self.equipment,
            "IsOrderLinkingSupported": int(self.is_order_linking_supported)
            if self.is_order_linking_supported is not None
            else None,
            "FunctionalLocation": self.functional_location,
            "ReasonGroups": self.reason_groups,
            "SetPoint": self.set_point,
            "Teams": self.teams,
        }

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> "Equipment":
        record = record or {}
        raw_is_last_unit = record.get("IsLastUnit")
        if isinstance(raw_is_last_unit, (list, tuple)):
            raw_is_last_unit = raw_is_last_unit[0]
        return cls(
            equipment_id=_to_int(record.get("ID") or record.get("EquipmentID")),
            name=record.get("Name"),
            description=record.get("Description"),
            alternate_name=record.get("AlternateName"),
            code=record.get("Code"),
            equipment_parent_id=_to_int(record.get("EquipmentParentID")),
            parent_name=record.get("parentname") or record.get("ParentName"),
            work_unit_thing_name=record.get("WorkUnitThingName"),
            production_count_multiplier=_to_float(
                record.get("ProductionCountMultiplier")
            ),
            is_first_unit=_to_int(record.get("IsFirstUnit")),
            is_last_unit=_to_int(raw_is_last_unit or record.get("IsLast")),
            equipment_type=record.get("EquipmentType"),
            reason_tree=record.get("ReasonTree"),
            has_children=bool(record.get("HasChildren"))
            if record.get("HasChildren") is not None
            else None,
            department_id=_to_int(record.get("DepartmentID")),
            equipment_number=record.get("EquipmentNumber"),
            equipment=record.get("Equipment"),
            is_order_linking_supported=bool(record.get("IsOrderLinkingSupported"))
            if record.get("IsOrderLinkingSupported") is not None
            else None,
            functional_location=record.get("FunctionalLocation"),
            reason_groups=record.get("ReasonGroups"),
            set_point=_to_float(record.get("SetPoint")),
            teams=record.get("Teams"),
        )

    def to_choice(self) -> Dict[str, Any]:
        equipment_type = (self.equipment_type or "Unknown").strip()
        if equipment_type.lower() == "workunit":
            label = f"{self.name} (Machine)"
        else:
            label = f"{self.name} ({equipment_type})"
        return {
            "label": label,
            "value": self.equipment_id,
            "EquipmentType": self.equipment_type,
        }


@dataclass
class EquipmentDropdown(object):
    value: Optional[int]
    label: str
    equipment_type: Optional[str] = None
    department_id: Optional[int] = None
    functional_location: Optional[str] = None
    equipment_number: Optional[str] = None
    code: Optional[str] = None

    @classmethod
    def from_equipment(cls, equipment: Equipment) -> "EquipmentDropdown":
        choice = equipment.to_choice()
        return cls(
            value=choice.get("value"),
            label=choice.get("label", equipment.name or ""),
            equipment_type=equipment.equipment_type,
            department_id=equipment.department_id,
            functional_location=equipment.functional_location,
            equipment_number=equipment.equipment_number,
            code=equipment.code,
        )

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> "EquipmentDropdown":
        equipment = Equipment.from_record(record)
        return cls.from_equipment(equipment)

    def to_record(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "value": self.value,
            "EquipmentType": self.equipment_type,
            "DepartmentID": self.department_id,
            "FunctionalLocation": self.functional_location,
            "EquipmentNumber": self.equipment_number,
            "Code": self.code,
        }


@dataclass
class EquipmentUpsert(object):
    name: str
    description: Optional[str] = None
    alternate_name: Optional[str] = None
    code: Optional[str] = None
    equipment_type_id: Optional[int] = None
    equipment_parent_id: Optional[int] = None
    is_consumption_point: int = 0
    is_production_point: int = 0
    consumption_cycle: Optional[float] = None
    production_cycle: Optional[float] = None
    location_id: Optional[int] = None
    shift_schedule_id: Optional[int] = None
    queqe_time: Optional[float] = None
    wait_time: Optional[float] = None
    work_center_id: Optional[int] = None
    template_id: Optional[int] = None
    department_id: Optional[int] = None
    sort_order: int = 0
    inserted_by: Optional[str] = None
    updated_by: Optional[str] = None
    is_deleted: int = 0
    equipment_class_id: Optional[int] = None
    work_unit_thing_name: Optional[str] = None
    production_count_multiplier: Optional[float] = 1
    is_first_unit: int = 0
    is_last_unit: int = 0
    equipment_number: Optional[str] = None
    functional_location: Optional[str] = None
    record_id: Optional[int] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "EquipmentUpsert":
        payload = payload or {}
        defaults = {
            "IsConsumptionPoint": 0,
            "IsProductionPoint": 0,
            "ConsumptionCycle": None,
            "ProductionCycle": None,
            "LocationID": None,
            "ShiftScheduleID": None,
            "QueqeTime": 0,
            "WaitTime": 0,
            "WorkCenterID": None,
            "TemplateID": None,
            "DepartmentID": None,
            "SortOrder": 0,
            "InsertedBy": payload.get("InsertedBy") or payload.get("UpdatedBy"),
            "UpdatedBy": payload.get("UpdatedBy"),
            "IsDeleted": payload.get("IsDeleted", 0),
            "EquipmentClassID": payload.get("EquipmentClassID"),
            "WorkUnitThingName": payload.get("WorkUnitThingName"),
            "ProductionCountMultiplier": payload.get("ProductionCountMultiplier", 1),
            "IsFirstUnit": payload.get("IsFirstUnit", 0),
            "IsLastUnit": payload.get("IsLastUnit", 0),
            "EquipmentNumber": payload.get("EquipmentNumber"),
            "FunctionalLocation": payload.get("FunctionalLocation"),
        }
        data = dict(defaults)
        data.update(payload)
        return cls(
            name=data.get("Name"),
            description=data.get("Description"),
            alternate_name=data.get("AlternateName"),
            code=data.get("Code"),
            equipment_type_id=_to_int(data.get("EquipmentTypeID")),
            equipment_parent_id=_to_int(data.get("EquipmentParentID")),
            is_consumption_point=_to_int(data.get("IsConsumptionPoint") or 0) or 0,
            is_production_point=_to_int(data.get("IsProductionPoint") or 0) or 0,
            consumption_cycle=_to_float(data.get("ConsumptionCycle")),
            production_cycle=_to_float(data.get("ProductionCycle")),
            location_id=_to_int(data.get("LocationID")),
            shift_schedule_id=_to_int(data.get("ShiftScheduleID")),
            queqe_time=_to_float(data.get("QueqeTime")),
            wait_time=_to_float(data.get("WaitTime")),
            work_center_id=_to_int(data.get("WorkCenterID")),
            template_id=_to_int(data.get("TemplateID")),
            department_id=_to_int(data.get("DepartmentID")),
            sort_order=_to_int(data.get("SortOrder") or 0) or 0,
            inserted_by=data.get("InsertedBy"),
            updated_by=data.get("UpdatedBy"),
            is_deleted=_to_int(data.get("IsDeleted") or 0) or 0,
            equipment_class_id=_to_int(data.get("EquipmentClassID")),
            work_unit_thing_name=data.get("WorkUnitThingName"),
            production_count_multiplier=_to_float(
                data.get("ProductionCountMultiplier") or 1
            )
            or 1,
            is_first_unit=_to_int(data.get("IsFirstUnit") or 0) or 0,
            is_last_unit=_to_int(data.get("IsLastUnit") or 0) or 0,
            equipment_number=data.get("EquipmentNumber"),
            functional_location=data.get("FunctionalLocation"),
            record_id=_to_int(data.get("ID") or data.get("EquipmentID")),
        )

    def to_record(self) -> Dict[str, Any]:
        record = {
            "ID": self.record_id,
            "Name": self.name,
            "Description": self.description,
            "AlternateName": self.alternate_name,
            "Code": self.code,
            "EquipmentTypeID": self.equipment_type_id,
            "EquipmentParentID": self.equipment_parent_id,
            "IsConsumptionPoint": self.is_consumption_point,
            "IsProductionPoint": self.is_production_point,
            "ConsumptionCycle": self.consumption_cycle,
            "ProductionCycle": self.production_cycle,
            "LocationID": self.location_id,
            "ShiftScheduleID": self.shift_schedule_id,
            "QueqeTime": self.queqe_time,
            "WaitTime": self.wait_time,
            "WorkCenterID": self.work_center_id,
            "TemplateID": self.template_id,
            "DepartmentID": self.department_id,
            "SortOrder": self.sort_order,
            "InsertedBy": self.inserted_by,
            "UpdatedBy": self.updated_by,
            "IsDeleted": self.is_deleted,
            "EquipmentClassID": self.equipment_class_id,
            "WorkUnitThingName": self.work_unit_thing_name,
            "ProductionCountMultiplier": self.production_count_multiplier,
            "IsFirstUnit": self.is_first_unit,
            "IsLastUnit": self.is_last_unit,
            "EquipmentNumber": self.equipment_number,
            "FunctionalLocation": self.functional_location,
        }
        return record


@dataclass
class Department(object):
    department_id: Optional[int] = None
    row_id: Optional[int] = None
    row_version: Optional[int] = None
    department_name: Optional[str] = None
    description: Optional[str] = None
    department_parent_id: Optional[int] = None
    department_type_id: Optional[int] = None
    department_type: Optional[str] = None
    category: Optional[int] = None
    sort_order: Optional[int] = None
    is_deleted: Optional[int] = None
    equipment_id: Optional[int] = None
    area: Optional[str] = None
    equipment_name: Optional[str] = None
    insert_time: Any = None
    inserted_by: Optional[str] = None
    update_time: Any = None
    updated_by: Optional[str] = None
    job_order_completion_threshold: Optional[float] = None
    alternate_name: Optional[str] = None
    department_number: Optional[str] = None
    department: Optional[str] = None
    is_first: Optional[int] = None
    is_last: Optional[int] = None
    is_order_linking_supported: Optional[int] = None
    functional_location: Optional[str] = None
    workstation_optimization: Optional[str] = None

    def to_record(self) -> Dict[str, Any]:
        return {
            "DepartmentID": self.department_id,
            "RowID": self.row_id,
            "RowVersion": self.row_version,
            "DepartmentName": self.department_name,
            "Description": self.description,
            "DepartmentParentID": self.department_parent_id,
            "DepartmentTypeID": self.department_type_id,
            "DepartmentType": self.department_type,
            "Category": self.category,
            "SortOrder": self.sort_order,
            "IsDeleted": self.is_deleted,
            "EquipmentID": self.equipment_id,
            "Area": self.area,
            "EquipmentName": self.equipment_name,
            "InsertTime": self.insert_time,
            "InsertedBy": self.inserted_by,
            "UpdateTime": self.update_time,
            "UpdatedBy": self.updated_by,
            "JobOrderCompletionThreshold": self.job_order_completion_threshold,
            "AlternateName": self.alternate_name,
            "DepartmentNumber": self.department_number,
            "Department": self.department,
            "IsFirst": self.is_first,
            "IsLast": self.is_last,
            "IsOrderLinkingSupported": self.is_order_linking_supported,
            "FunctionalLocation": self.functional_location,
            "WorkstationOptimization": self.workstation_optimization,
        }

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> "Department":
        record = record or {}
        return cls(
            department_id=_to_int(record.get("DepartmentID")),
            row_id=_to_int(record.get("RowID")),
            row_version=_to_int(record.get("RowVersion")),
            department_name=record.get("DepartmentName"),
            description=record.get("Description"),
            department_parent_id=_to_int(record.get("DepartmentParentID")),
            department_type_id=_to_int(record.get("DepartmentTypeID")),
            department_type=record.get("DepartmentType"),
            category=_to_int(record.get("Category")),
            sort_order=_to_int(record.get("SortOrder")),
            is_deleted=_to_int(record.get("IsDeleted")),
            equipment_id=_to_int(record.get("EquipmentID")),
            area=record.get("Area"),
            equipment_name=record.get("EquipmentName"),
            insert_time=record.get("InsertTime"),
            inserted_by=record.get("InsertedBy"),
            update_time=record.get("UpdateTime"),
            updated_by=record.get("UpdatedBy"),
            job_order_completion_threshold=_to_float(
                record.get("JobOrderCompletionThreshold")
            ),
            alternate_name=record.get("AlternateName"),
            department_number=record.get("DepartmentNumber"),
            department=record.get("Department"),
            is_first=_to_int(record.get("IsFirst")),
            is_last=_to_int(record.get("IsLast")),
            is_order_linking_supported=_to_int(record.get("IsOrderLinkingSupported")),
            functional_location=record.get("FunctionalLocation"),
            workstation_optimization=record.get("WorkstationOptimization"),
        )

    def to_choice(self) -> Dict[str, Any]:
        return {"label": self.department_name, "value": self.department_id}


@dataclass
class DepartmentUpsert(object):
    name: str
    description: Optional[str] = None
    category: Optional[int] = None
    sort_order: int = 1
    is_deleted: int = 0
    department_type_id: Optional[int] = None
    department_parent_id: Optional[int] = None
    is_order_linking_supported: Optional[int] = None
    equipment_id: Optional[int] = None
    inserted_by: Optional[str] = None
    updated_by: Optional[str] = None
    job_order_completion_threshold: Optional[float] = None
    alternate_name: Optional[str] = None
    department_number: Optional[str] = None
    functional_location: Optional[str] = None
    workstation_optimization: Optional[str] = None
    department_id: Optional[int] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "DepartmentUpsert":
        payload = payload or {}
        defaults = {
            "SortOrder": payload.get("SortOrder", 1) or 1,
            "IsDeleted": payload.get("IsDeleted", 0) or 0,
        }
        data = dict(defaults)
        data.update(payload)
        return cls(
            name=data.get("Name"),
            description=data.get("Description"),
            category=_to_int(data.get("Category")),
            sort_order=_to_int(data.get("SortOrder") or 1) or 1,
            is_deleted=_to_int(data.get("IsDeleted") or 0) or 0,
            department_type_id=_to_int(data.get("DepartmentTypeID")),
            department_parent_id=_to_int(data.get("DepartmentParentID")),
            is_order_linking_supported=_to_int(data.get("IsOrderLinkingSupported")),
            equipment_id=_to_int(data.get("EquipmentID")),
            inserted_by=data.get("InsertedBy"),
            updated_by=data.get("UpdatedBy"),
            job_order_completion_threshold=_to_float(
                data.get("JobOrderCompletionThreshold")
            ),
            alternate_name=data.get("AlternateName"),
            department_number=data.get("DepartmentNumber"),
            functional_location=data.get("FunctionalLocation"),
            workstation_optimization=data.get("WorkstationOptimization"),
            department_id=_to_int(data.get("DepartmentID")),
        )

    def to_record(self) -> Dict[str, Any]:
        return {
            "DepartmentID": self.department_id,
            "Name": self.name,
            "Description": self.description,
            "Category": self.category,
            "SortOrder": self.sort_order,
            "IsDeleted": self.is_deleted,
            "DepartmentTypeID": self.department_type_id,
            "DepartmentParentID": self.department_parent_id,
            "IsOrderLinkingSupported": self.is_order_linking_supported,
            "EquipmentID": self.equipment_id,
            "InsertedBy": self.inserted_by,
            "UpdatedBy": self.updated_by,
            "JobOrderCompletionThreshold": self.job_order_completion_threshold,
            "AlternateName": self.alternate_name,
            "DepartmentNumber": self.department_number,
            "FunctionalLocation": self.functional_location,
            "WorkstationOptimization": self.workstation_optimization,
        }


@dataclass
class DepartmentDropdown(object):
    value: Optional[int]
    label: Optional[str]
    department_parent_id: Optional[int] = None
    department_type_id: Optional[int] = None
    department_number: Optional[str] = None

    @classmethod
    def from_department(cls, department: Department) -> "DepartmentDropdown":
        record = department.to_record()
        return cls(
            value=record.get("DepartmentID"),
            label=record.get("DepartmentName"),
            department_parent_id=record.get("DepartmentParentID"),
            department_type_id=record.get("DepartmentTypeID"),
            department_number=record.get("DepartmentNumber"),
        )

    def to_record(self) -> Dict[str, Any]:
        return {
            "DepartmentID": self.value,
            "DepartmentName": self.label,
            "DepartmentParentID": self.department_parent_id,
            "DepartmentTypeID": self.department_type_id,
            "DepartmentNumber": self.department_number,
            "label": self.label,
            "value": self.value,
        }


@dataclass
class EquipmentClass(object):
    equipment_class_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    alternate_name: Optional[str] = None
    code: Optional[str] = None
    training_setpoint_duration: Optional[float] = None
    equipment_class_number: Optional[str] = None

    def to_record(self) -> Dict[str, Any]:
        return {
            "ID": self.equipment_class_id,
            "Name": self.name,
            "Description": self.description,
            "AlternateName": self.alternate_name,
            "Code": self.code,
            "TrainingSetpointDuration": self.training_setpoint_duration,
            "EquipmentClassNumber": self.equipment_class_number,
            "label": self.name,
            "value": self.equipment_class_id,
        }

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> "EquipmentClass":
        record = record or {}
        return cls(
            equipment_class_id=_to_int(record.get("ID") or record.get("EquipmentClassID")),
            name=record.get("Name"),
            description=record.get("Description"),
            alternate_name=record.get("AlternateName"),
            code=record.get("Code"),
            training_setpoint_duration=_to_float(record.get("TrainingSetpointDuration")),
            equipment_class_number=record.get("EquipmentClassNumber"),
        )


@dataclass
class EquipmentClassUpsert(object):
    name: str
    description: Optional[str] = None
    alternate_name: Optional[str] = None
    code: Optional[str] = None
    inserted_by: Optional[str] = None
    is_deleted: int = 0
    training_setpoint_duration: Optional[float] = None
    equipment_class_number: Optional[str] = None

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "EquipmentClassUpsert":
        payload = payload or {}
        defaults = {"IsDeleted": 0, "TrainingSetpointDuration": 1}
        data = dict(defaults)
        data.update(payload)
        return cls(
            name=data.get("Name"),
            description=data.get("Description"),
            alternate_name=data.get("AlternateName"),
            code=data.get("Code"),
            inserted_by=data.get("InsertedBy"),
            is_deleted=_to_int(data.get("IsDeleted") or 0) or 0,
            training_setpoint_duration=_to_float(data.get("TrainingSetpointDuration")),
            equipment_class_number=data.get("EquipmentClassNumber"),
        )

    def to_record(self) -> Dict[str, Any]:
        return {
            "Name": self.name,
            "Description": self.description,
            "AlternateName": self.alternate_name,
            "Code": self.code,
            "InsertedBy": self.inserted_by,
            "IsDeleted": self.is_deleted,
            "TrainingSetpointDuration": self.training_setpoint_duration,
            "EquipmentClassNumber": self.equipment_class_number,
        }


@dataclass
class MachineDropdown(object):
    equipment_id: Optional[int]
    machine: Optional[str]
    equipment_class_id: Optional[int] = None
    machine_class: Optional[str] = None
    work_station_id: Optional[int] = None
    work_station: Optional[str] = None
    line_id: Optional[int] = None
    line: Optional[str] = None
    work_center_id: Optional[int] = None
    work_center: Optional[str] = None
    alternate_name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    equipment_number: Optional[str] = None
    equipment: Optional[str] = None
    functional_location: Optional[str] = None

    @classmethod
    def from_record(cls, record: Dict[str, Any]) -> "MachineDropdown":
        record = record or {}
        return cls(
            equipment_id=_to_int(record.get("EquipmentID")),
            machine=record.get("Machine") or record.get("Name"),
            equipment_class_id=_to_int(record.get("EquipmentClassID")),
            machine_class=record.get("MachineClass"),
            work_station_id=_to_int(record.get("WorkStationID")),
            work_station=record.get("WorkStation"),
            line_id=_to_int(record.get("LineID")),
            line=record.get("Line"),
            work_center_id=_to_int(record.get("WorkCenterID")),
            work_center=record.get("WorkCenter"),
            alternate_name=record.get("AlternateName"),
            code=record.get("Code"),
            description=record.get("Description"),
            equipment_number=record.get("EquipmentNumber"),
            equipment=record.get("Equipment"),
            functional_location=record.get("FunctionalLocation"),
        )

    def to_record(self) -> Dict[str, Any]:
        return {
            "EquipmentID": self.equipment_id,
            "Machine": self.machine,
            "EquipmentClassID": self.equipment_class_id,
            "MachineClass": self.machine_class,
            "WorkStationID": self.work_station_id,
            "WorkStation": self.work_station,
            "LineID": self.line_id,
            "Line": self.line,
            "WorkCenterID": self.work_center_id,
            "WorkCenter": self.work_center,
            "AlternateName": self.alternate_name,
            "Code": self.code,
            "Description": self.description,
            "EquipmentNumber": self.equipment_number,
            "Equipment": self.equipment,
            "FunctionalLocation": self.functional_location,
            "label": self.machine,
            "value": self.equipment_id,
        }


@dataclass
class WorkstationSortOrder(object):
    department_id: int
    sort_order: int

    @staticmethod
    def from_sequence(sequence: Iterable[Dict[str, Any]]) -> List["WorkstationSortOrder"]:
        results = []
        for item in sequence or []:
            try:
                dept_id = _to_int(item.get("DepartmentID") or item.get("ID"))
                order = _to_int(item.get("SortOrder"))
                if dept_id is None or order is None:
                    continue
                results.append(
                    WorkstationSortOrder(department_id=dept_id, sort_order=order)
                )
            except Exception:
                continue
        return results

    def to_record(self) -> Dict[str, Any]:
        return {"DepartmentID": self.department_id, "SortOrder": self.sort_order}
