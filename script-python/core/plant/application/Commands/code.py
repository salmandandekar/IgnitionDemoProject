"""Command objects representing write use-cases for the plant bounded context."""

from core.plant.domain.Entities import code as entities

EquipmentUpsert = entities.EquipmentUpsert
DepartmentUpsert = entities.DepartmentUpsert
EquipmentClassUpsert = entities.EquipmentClassUpsert
WorkstationSortOrder = entities.WorkstationSortOrder


class CreateEquipmentCommand(object):
    def __init__(self, user_id, payload):
        self.user_id = user_id
        self.equipment = EquipmentUpsert.from_dict(payload)


class UpdateEquipmentCommand(object):
    def __init__(self, user_id, payload):
        self.user_id = user_id
        self.equipment = EquipmentUpsert.from_dict(payload)


class DeleteEquipmentCommand(object):
    def __init__(self, user_id, equipment_id):
        self.user_id = user_id
        self.equipment_id = equipment_id


class CreateDepartmentCommand(object):
    def __init__(self, user_id, payload):
        self.user_id = user_id
        self.department = DepartmentUpsert.from_dict(payload)


class UpdateDepartmentCommand(object):
    def __init__(self, user_id, payload):
        self.user_id = user_id
        self.department = DepartmentUpsert.from_dict(payload)


class DeleteDepartmentCommand(object):
    def __init__(self, user_id, department_id, updated_by):
        self.user_id = user_id
        self.department_id = department_id
        self.updated_by = updated_by


class InsertEquipmentClassCommand(object):
    def __init__(self, user_id, payload):
        self.user_id = user_id
        self.equipment_class = EquipmentClassUpsert.from_dict(payload)


class UpdateWorkstationSortOrderCommand(object):
    def __init__(self, user_id, sequence):
        self.user_id = user_id
        self.sort_orders = WorkstationSortOrder.from_sequence(sequence)


class BulkUploadMachinesCommand(object):
    def __init__(self, user_id, json_payload, clock_id):
        self.user_id = user_id
        self.json_payload = json_payload
        self.clock_id = clock_id
