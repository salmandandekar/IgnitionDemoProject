"""Query objects representing read use-cases for the plant bounded context."""


class GetEquipmentTreeQuery(object):
    def __init__(self, user_id):
        self.user_id = user_id


class GetEquipmentDropdownQuery(object):
    def __init__(self, user_id):
        self.user_id = user_id


class GetWorkcenterDropdownQuery(object):
    def __init__(self, user_id):
        self.user_id = user_id


class GetMachineDropdownQuery(object):
    def __init__(self, user_id, equipment_id=None, workstation_id=None, workcenter_id=None):
        self.user_id = user_id
        self.filters = {
            "EquipmentID": equipment_id,
            "WorkStationID": workstation_id,
            "WorkCenterID": workcenter_id,
        }


class GetDepartmentsQuery(object):
    def __init__(self, user_id, department_id=None):
        self.user_id = user_id
        self.department_id = department_id


class GetDepartmentDropdownQuery(object):
    def __init__(self, user_id, department_id=None):
        self.user_id = user_id
        self.department_id = department_id


class GetEquipmentDetailsQuery(object):
    def __init__(self, user_id, equipment_id=None, workstation_id=None, workcenter_id=None):
        self.user_id = user_id
        self.filters = {
            "EquipmentID": equipment_id,
            "WorkStationID": workstation_id,
            "WorkCenterID": workcenter_id,
        }


class GetEquipmentClassDropdownQuery(object):
    def __init__(self, user_id):
        self.user_id = user_id


class GetEquipmentNameQuery(object):
    def __init__(self, user_id, plant_model_type):
        self.user_id = user_id
        self.plant_model_type = plant_model_type


class GetWorkstationFromMachineQuery(object):
    def __init__(self, user_id, equipment_id):
        self.user_id = user_id
        self.equipment_id = equipment_id


class ExportMachinesQuery(object):
    def __init__(self, user_id, equipment_id=None, workstation_id=None, workcenter_id=None):
        self.user_id = user_id
        self.filters = {
            "EquipmentID": equipment_id,
            "WorkStationID": workstation_id,
            "WorkCenterID": workcenter_id,
        }


class FilterValidMachinesQuery(object):
    def __init__(self, machines_data):
        self.machines_data = machines_data
