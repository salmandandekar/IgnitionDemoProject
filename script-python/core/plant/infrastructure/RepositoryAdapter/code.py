"""Repository adapter bridging plant aggregate operations with stored procedures."""

from common.cache.CacheManager import code as cache
from common.logging.LogFactory import code as LogFactory
from core.plant.domain.Entities import code as entities
from core.plant.ports.RepositoryPort import code as port

Equipment = entities.Equipment
EquipmentDropdown = entities.EquipmentDropdown
EquipmentUpsert = entities.EquipmentUpsert
Department = entities.Department
DepartmentDropdown = entities.DepartmentDropdown
MachineDropdown = entities.MachineDropdown
EquipmentClass = entities.EquipmentClass

_LOG = LogFactory.get_logger("PlantRepository")
_CACHE_BUCKET = "plant"
_DS_CACHE_PREFIX = "datasource"

SP_GET_EQUIPMENT_TREE = "usp_S_GetEquipmentDetails"
SP_GET_EQUIPMENT_DROPDOWN = "usp_S_GetEquipmentDetailsAll"
SP_GET_WORKCENTER_DROPDOWN = "usp_S_GetEquipmentDetails"
SP_GET_DEPARTMENTS = "usp_S_GetDepartment"
SP_GET_EQUIPMENT = "usp_S_GetEquipment"
SP_GET_EQUIPMENT_CLASS = "usp_S_GetEquipmentClass"
SP_INSERT_EQUIPMENT = "usp_I_InsertEquipment"
SP_UPDATE_EQUIPMENT = "usp_U_UpdateEquipment"
SP_DELETE_EQUIPMENT = "usp_D_DeleteEquipment"
SP_INSERT_DEPARTMENT = "usp_I_InsertDepartment"
SP_UPDATE_DEPARTMENT = "usp_U_UpdateDepartment"
SP_DELETE_DEPARTMENT = "usp_D_DeleteDepartment"
SP_INSERT_EQUIPMENT_CLASS = "usp_I_InsertEquipmentClass"
SP_GET_EQUIPMENT_NAME = "usp_S_GetPlantModelEquipmentName"
SP_GET_WORKSTATION_FROM_MACHINE = "usp_S_GetWorkstationFromMachine"
SP_UPDATE_WORKSTATION_SORT_ORDER = "usp_U_UpdateWorkstationSortOrder"
SP_BULK_UPLOAD_MACHINES = "usp_C_BulkUploadMaterials"


class PlantRepositoryAdapter(port.PlantRepositoryPort):
    def __init__(self):
        self._log = _LOG

    # ------------------------------------------------------------------
    # Datasource resolution helpers
    # ------------------------------------------------------------------
    def _resolve_datasource(self, user_id):
        cache_key = "%s:%s" % (_DS_CACHE_PREFIX, user_id)
        cached = cache.get(_CACHE_BUCKET, cache_key)
        if cached:
            return cached

        datasource = None
        try:
            from DataSource import GetDataSources

            datasource = GetDataSources.get_data_source(user_id)
        except Exception:
            datasource = None

        if not datasource:
            try:
                from infrastructure.DatabaseConfig import datasource_name

                datasource = datasource_name()
            except Exception:
                datasource = None

        cache.put(_CACHE_BUCKET, cache_key, datasource, ttl_seconds=30)
        return datasource

    # ------------------------------------------------------------------
    # Ignition helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _run_query(statement, params, datasource):
        try:
            from system.db import runPrepQuery

            if datasource:
                return runPrepQuery(statement, params, datasource)
            return runPrepQuery(statement, params)
        except Exception:
            return []

    @staticmethod
    def _dataset_to_dicts(dataset):
        if dataset is None:
            return []
        if isinstance(dataset, list):
            return [dict(row) if isinstance(row, dict) else row for row in dataset]
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

    @classmethod
    def _first_row(cls, dataset):
        rows = cls._dataset_to_dicts(dataset)
        return rows[0] if rows else {}

    # ------------------------------------------------------------------
    # Query implementations
    # ------------------------------------------------------------------
    def fetch_equipment_tree(self, user_id):
        ds = self._resolve_datasource(user_id)
        statement = "EXEC %s" % SP_GET_EQUIPMENT_TREE
        rows = self._dataset_to_dicts(self._run_query(statement, [], ds))
        return [Equipment.from_record(row) for row in rows]

    def fetch_equipment_dropdown(self, user_id):
        ds = self._resolve_datasource(user_id)
        statement = "EXEC %s" % SP_GET_EQUIPMENT_DROPDOWN
        rows = self._dataset_to_dicts(self._run_query(statement, [], ds))
        return [EquipmentDropdown.from_record(row) for row in rows]

    def fetch_workcenter_dropdown(self, user_id):
        ds = self._resolve_datasource(user_id)
        statement = "EXEC %s" % SP_GET_WORKCENTER_DROPDOWN
        rows = self._dataset_to_dicts(self._run_query(statement, [], ds))
        return [EquipmentDropdown.from_record(row) for row in rows]

    def fetch_machine_dropdown(self, filters, user_id):
        ds = self._resolve_datasource(user_id)
        params = [
            filters.get("EquipmentID"),
            filters.get("WorkStationID"),
            filters.get("WorkCenterID"),
        ]
        statement = "EXEC %s @EquipmentID=?, @WorkStationID=?, @WorkCenterID=?" % SP_GET_EQUIPMENT
        rows = self._dataset_to_dicts(self._run_query(statement, params, ds))
        return [MachineDropdown.from_record(row) for row in rows]

    def fetch_departments(self, department_id, user_id):
        ds = self._resolve_datasource(user_id)
        statement = "EXEC %s @DepartmentID=?" % SP_GET_DEPARTMENTS
        rows = self._dataset_to_dicts(self._run_query(statement, [department_id], ds))
        return [Department.from_record(row) for row in rows]

    def fetch_department_dropdown(self, department_id, user_id):
        departments = self.fetch_departments(department_id, user_id)
        return [DepartmentDropdown.from_department(dep) for dep in departments]

    def fetch_equipment_details(self, filters, user_id):
        ds = self._resolve_datasource(user_id)
        params = [
            filters.get("EquipmentID"),
            filters.get("WorkStationID"),
            filters.get("WorkCenterID"),
        ]
        statement = "EXEC %s @EquipmentID=?, @WorkStationID=?, @WorkCenterID=?" % SP_GET_EQUIPMENT
        rows = self._dataset_to_dicts(self._run_query(statement, params, ds))
        return [MachineDropdown.from_record(row) for row in rows]

    def fetch_equipment_class_dropdown(self, user_id):
        ds = self._resolve_datasource(user_id)
        statement = "EXEC %s" % SP_GET_EQUIPMENT_CLASS
        rows = self._dataset_to_dicts(self._run_query(statement, [], ds))
        return [EquipmentClass.from_record(row) for row in rows]

    def fetch_equipment_name(self, plant_model_type, user_id):
        ds = self._resolve_datasource(user_id)
        statement = "EXEC %s @PlantModelType=?" % SP_GET_EQUIPMENT_NAME
        result = self._run_query(statement, [plant_model_type], ds)
        first = self._first_row(result)
        if isinstance(first, dict):
            return list(first.values())[0] if first else None
        if isinstance(result, list) and result:
            row = result[0]
            if isinstance(row, dict):
                return list(row.values())[0] if row else None
            if isinstance(row, (list, tuple)):
                return row[0] if row else None
        return first or None

    def fetch_workstation_from_machine(self, equipment_id, user_id):
        ds = self._resolve_datasource(user_id)
        statement = "EXEC %s @EquipmentID=?" % SP_GET_WORKSTATION_FROM_MACHINE
        return self._dataset_to_dicts(self._run_query(statement, [equipment_id], ds))

    # ------------------------------------------------------------------
    # Command implementations
    # ------------------------------------------------------------------
    def insert_equipment(self, record, user_id):
        ds = self._resolve_datasource(user_id)
        params = [
            record.get("Name"),
            record.get("Description"),
            record.get("AlternateName"),
            record.get("Code"),
            record.get("EquipmentTypeID"),
            record.get("EquipmentParentID"),
            record.get("IsConsumptionPoint"),
            record.get("IsProductionPoint"),
            record.get("ConsumptionCycle"),
            record.get("ProductionCycle"),
            record.get("LocationID"),
            record.get("ShiftScheduleID"),
            record.get("QueqeTime"),
            record.get("WaitTime"),
            record.get("WorkCenterID"),
            record.get("TemplateID"),
            record.get("DepartmentID"),
            record.get("SortOrder"),
            record.get("InsertedBy"),
            record.get("UpdatedBy"),
            record.get("IsDeleted"),
            record.get("EquipmentClassID"),
            record.get("WorkUnitThingName"),
            record.get("ProductionCountMultiplier"),
            record.get("IsFirstUnit"),
            record.get("IsLastUnit"),
            record.get("EquipmentNumber"),
            record.get("FunctionalLocation"),
        ]
        statement = "EXEC %s " % SP_INSERT_EQUIPMENT + ", ".join([
            "@Name=?",
            "@Description=?",
            "@AlternateName=?",
            "@Code=?",
            "@EquipmentTypeID=?",
            "@EquipmentParentID=?",
            "@IsConsumptionPoint=?",
            "@IsProductionPoint=?",
            "@ConsumptionCycle=?",
            "@ProductionCycle=?",
            "@LocationID=?",
            "@ShiftScheduleID=?",
            "@QueqeTime=?",
            "@WaitTime=?",
            "@WorkCenterID=?",
            "@TemplateID=?",
            "@DepartmentID=?",
            "@SortOrder=?",
            "@InsertedBy=?",
            "@UpdatedBy=?",
            "@IsDeleted=?",
            "@EquipmentClassID=?",
            "@WorkUnitThingName=?",
            "@ProductionCountMultiplier=?",
            "@IsFirstUnit=?",
            "@IsLastUnit=?",
            "@EquipmentNumber=?",
            "@FunctionalLocation=?",
        ])
        result = self._run_query(statement, params, ds)
        return self._first_row(result)

    def update_equipment(self, record, user_id):
        ds = self._resolve_datasource(user_id)
        params = [
            record.get("ID"),
            record.get("Name"),
            record.get("Description"),
            record.get("AlternateName"),
            record.get("Code"),
            record.get("EquipmentTypeID"),
            record.get("EquipmentParentID"),
            record.get("IsConsumptionPoint"),
            record.get("IsProductionPoint"),
            record.get("ConsumptionCycle"),
            record.get("ProductionCycle"),
            record.get("LocationID"),
            record.get("ShiftScheduleID"),
            record.get("QueqeTime"),
            record.get("WaitTime"),
            record.get("WorkCenterID"),
            record.get("TemplateID"),
            record.get("DepartmentID"),
            record.get("SortOrder"),
            record.get("UpdatedBy"),
            record.get("IsDeleted"),
            record.get("EquipmentClassID"),
            record.get("WorkUnitThingName"),
            record.get("ProductionCountMultiplier"),
            record.get("IsFirstUnit"),
            record.get("IsLastUnit"),
            record.get("FunctionalLocation"),
        ]
        statement = "EXEC %s " % SP_UPDATE_EQUIPMENT + ", ".join([
            "@ID=?",
            "@Name=?",
            "@Description=?",
            "@AlternateName=?",
            "@Code=?",
            "@EquipmentTypeID=?",
            "@EquipmentParentID=?",
            "@IsConsumptionPoint=?",
            "@IsProductionPoint=?",
            "@ConsumptionCycle=?",
            "@ProductionCycle=?",
            "@LocationID=?",
            "@ShiftScheduleID=?",
            "@QueqeTime=?",
            "@WaitTime=?",
            "@WorkCenterID=?",
            "@TemplateID=?",
            "@DepartmentID=?",
            "@SortOrder=?",
            "@UpdatedBy=?",
            "@IsDeleted=?",
            "@EquipmentClassID=?",
            "@WorkUnitThingName=?",
            "@ProductionCountMultiplier=?",
            "@IsFirstUnit=?",
            "@IsLastUnit=?",
            "@FunctionalLocation=?",
        ])
        result = self._run_query(statement, params, ds)
        return self._first_row(result)

    def delete_equipment(self, equipment_id, user_id):
        ds = self._resolve_datasource(user_id)
        statement = "EXEC %s @EquipmentID=?" % SP_DELETE_EQUIPMENT
        result = self._run_query(statement, [equipment_id], ds)
        return self._first_row(result)

    def insert_department(self, record, user_id):
        ds = self._resolve_datasource(user_id)
        params = [
            record.get("Name"),
            record.get("Description"),
            record.get("Category"),
            record.get("SortOrder"),
            record.get("IsDeleted"),
            record.get("DepartmentTypeID"),
            record.get("DepartmentParentID"),
            record.get("IsOrderLinkingSupported"),
            record.get("EquipmentID"),
            record.get("InsertedBy"),
            record.get("JobOrderCompletionThreshold"),
            record.get("AlternateName"),
            record.get("DepartmentNumber"),
            record.get("FunctionalLocation"),
            record.get("WorkstationOptimization"),
        ]
        statement = "EXEC %s " % SP_INSERT_DEPARTMENT + ", ".join([
            "@Name=?",
            "@Description=?",
            "@Category=?",
            "@SortOrder=?",
            "@IsDeleted=?",
            "@DepartmentTypeID=?",
            "@DepartmentParentID=?",
            "@IsOrderLinkingSupported=?",
            "@EquipmentID=?",
            "@InsertedBy=?",
            "@JobOrderCompletionThreshold=?",
            "@AlternateName=?",
            "@DepartmentNumber=?",
            "@FunctionalLocation=?",
            "@WorkstationOptimization=?",
        ])
        result = self._run_query(statement, params, ds)
        return self._first_row(result)

    def update_department(self, record, user_id):
        ds = self._resolve_datasource(user_id)
        params = [
            record.get("DepartmentID"),
            record.get("Name"),
            record.get("Description"),
            record.get("Category"),
            record.get("SortOrder"),
            record.get("IsDeleted"),
            record.get("DepartmentTypeID"),
            record.get("DepartmentParentID"),
            record.get("IsOrderLinkingSupported"),
            record.get("EquipmentID"),
            record.get("UpdatedBy"),
            record.get("JobOrderCompletionThreshold"),
            record.get("AlternateName"),
            record.get("FunctionalLocation"),
            record.get("WorkstationOptimization"),
        ]
        statement = "EXEC %s " % SP_UPDATE_DEPARTMENT + ", ".join([
            "@DepartmentID=?",
            "@Name=?",
            "@Description=?",
            "@Category=?",
            "@SortOrder=?",
            "@IsDeleted=?",
            "@DepartmentTypeID=?",
            "@DepartmentParentID=?",
            "@IsOrderLinkingSupported=?",
            "@EquipmentID=?",
            "@UpdatedBy=?",
            "@JobOrderCompletionThreshold=?",
            "@AlternateName=?",
            "@FunctionalLocation=?",
            "@WorkstationOptimization=?",
        ])
        result = self._run_query(statement, params, ds)
        return self._first_row(result)

    def delete_department(self, department_id, updated_by, user_id):
        ds = self._resolve_datasource(user_id)
        params = [department_id, updated_by]
        statement = "EXEC %s @DepartmentID=?, @UpdatedBy=?" % SP_DELETE_DEPARTMENT
        result = self._run_query(statement, params, ds)
        return self._first_row(result)

    def insert_equipment_class(self, record, user_id):
        ds = self._resolve_datasource(user_id)
        params = [
            record.get("Name"),
            record.get("Description"),
            record.get("AlternateName"),
            record.get("Code"),
            record.get("InsertedBy"),
            record.get("IsDeleted"),
            record.get("TrainingSetpointDuration"),
            record.get("EquipmentClassNumber"),
        ]
        statement = "EXEC %s " % SP_INSERT_EQUIPMENT_CLASS + ", ".join([
            "@Name=?",
            "@Description=?",
            "@AlternateName=?",
            "@Code=?",
            "@InsertedBy=?",
            "@IsDeleted=?",
            "@TrainingSetpointDuration=?",
            "@EquipmentClassNumber=?",
        ])
        result = self._run_query(statement, params, ds)
        return self._first_row(result)

    def update_workstation_sort_order(self, json_payload, user_id):
        ds = self._resolve_datasource(user_id)
        statement = "EXEC %s @JsonDept=?" % SP_UPDATE_WORKSTATION_SORT_ORDER
        return self._run_query(statement, [json_payload], ds)

    def bulk_upload_machines(self, json_payload, clock_id, user_id):
        ds = self._resolve_datasource(user_id)
        statement = "EXEC %s @JSONMaterialsList=?, @ClockID=?" % SP_BULK_UPLOAD_MACHINES
        result = self._run_query(statement, [json_payload, clock_id], ds)
        return self._first_row(result)
