"""Application façade for plant bounded context interactions."""

from common.logging.LogFactory import code as LogFactory
from core.plant.application.Commands import code as cmds
from core.plant.application.CommandHandlers import code as ch
from core.plant.application.Queries import code as queries
from core.plant.application.QueryHandlers import code as qh
from core.plant.infrastructure.RepositoryAdapter import code as repo

_LOG = LogFactory.get_logger("PlantController")


class PlantController(object):
    def __init__(self, user_id, repository=None):
        self.user_id = user_id
        self.repository = repository or repo.PlantRepositoryAdapter()

    # ----------------------------- Queries ---------------------------------
    def get_equipment_tree(self):
        q = queries.GetEquipmentTreeQuery(self.user_id)
        return qh.handle_get_equipment_tree(q, self.repository)

    def get_equipment_dropdown(self):
        q = queries.GetEquipmentDropdownQuery(self.user_id)
        return qh.handle_get_equipment_dropdown(q, self.repository)

    def get_workcenter_dropdown(self):
        q = queries.GetWorkcenterDropdownQuery(self.user_id)
        return qh.handle_get_workcenter_dropdown(q, self.repository)

    def get_machine_dropdown(self, equipment_id=None, workstation_id=None, workcenter_id=None):
        q = queries.GetMachineDropdownQuery(self.user_id, equipment_id, workstation_id, workcenter_id)
        return qh.handle_get_machine_dropdown(q, self.repository)

    def get_departments(self, department_id=None):
        q = queries.GetDepartmentsQuery(self.user_id, department_id)
        return qh.handle_get_departments(q, self.repository)

    def get_department_dropdown(self, department_id=None):
        q = queries.GetDepartmentDropdownQuery(self.user_id, department_id)
        return qh.handle_get_department_dropdown(q, self.repository)

    def get_equipment_details(self, equipment_id=None, workstation_id=None, workcenter_id=None):
        q = queries.GetEquipmentDetailsQuery(self.user_id, equipment_id, workstation_id, workcenter_id)
        return qh.handle_get_equipment_details(q, self.repository)

    def get_equipment_class_dropdown(self):
        q = queries.GetEquipmentClassDropdownQuery(self.user_id)
        return qh.handle_get_equipment_class_dropdown(q, self.repository)

    def get_equipment_name(self, plant_model_type):
        q = queries.GetEquipmentNameQuery(self.user_id, plant_model_type)
        return qh.handle_get_equipment_name(q, self.repository)

    def get_workstation_from_machine(self, equipment_id):
        q = queries.GetWorkstationFromMachineQuery(self.user_id, equipment_id)
        return qh.handle_get_workstation_from_machine(q, self.repository)

    def export_machines(self, equipment_id=None, workstation_id=None, workcenter_id=None):
        q = queries.ExportMachinesQuery(self.user_id, equipment_id, workstation_id, workcenter_id)
        return qh.handle_export_machines(q, self.repository)

    def filter_valid_machines(self, machines_data):
        q = queries.FilterValidMachinesQuery(machines_data)
        return qh.handle_filter_valid_machines(q)

    # ----------------------------- Commands --------------------------------
    def create_equipment(self, payload):
        command = cmds.CreateEquipmentCommand(self.user_id, payload)
        return ch.handle_create_equipment(command, self.repository)

    def update_equipment(self, payload):
        command = cmds.UpdateEquipmentCommand(self.user_id, payload)
        return ch.handle_update_equipment(command, self.repository)

    def delete_equipment(self, equipment_id):
        command = cmds.DeleteEquipmentCommand(self.user_id, equipment_id)
        return ch.handle_delete_equipment(command, self.repository)

    def create_department(self, payload):
        command = cmds.CreateDepartmentCommand(self.user_id, payload)
        return ch.handle_create_department(command, self.repository)

    def update_department(self, payload):
        command = cmds.UpdateDepartmentCommand(self.user_id, payload)
        return ch.handle_update_department(command, self.repository)

    def delete_department(self, department_id, updated_by):
        command = cmds.DeleteDepartmentCommand(self.user_id, department_id, updated_by)
        return ch.handle_delete_department(command, self.repository)

    def insert_equipment_class(self, payload):
        command = cmds.InsertEquipmentClassCommand(self.user_id, payload)
        return ch.handle_insert_equipment_class(command, self.repository)

    def update_workstation_sort_order(self, sequence):
        command = cmds.UpdateWorkstationSortOrderCommand(self.user_id, sequence)
        return ch.handle_update_workstation_sort_order(command, self.repository)

    def bulk_upload_machines(self, json_payload, clock_id):
        command = cmds.BulkUploadMachinesCommand(self.user_id, json_payload, clock_id)
        return ch.handle_bulk_upload_machines(command, self.repository)
