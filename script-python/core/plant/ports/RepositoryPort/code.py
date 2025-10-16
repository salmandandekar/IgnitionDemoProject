"""Abstraction for persistence operations required by the plant bounded context."""


class PlantRepositoryPort(object):
    def fetch_equipment_tree(self, user_id):
        raise NotImplementedError

    def fetch_equipment_dropdown(self, user_id):
        raise NotImplementedError

    def fetch_workcenter_dropdown(self, user_id):
        raise NotImplementedError

    def fetch_machine_dropdown(self, filters, user_id):
        raise NotImplementedError

    def fetch_departments(self, department_id, user_id):
        raise NotImplementedError

    def fetch_department_dropdown(self, department_id, user_id):
        raise NotImplementedError

    def fetch_equipment_details(self, filters, user_id):
        raise NotImplementedError

    def fetch_equipment_class_dropdown(self, user_id):
        raise NotImplementedError

    def fetch_equipment_name(self, plant_model_type, user_id):
        raise NotImplementedError

    def fetch_workstation_from_machine(self, equipment_id, user_id):
        raise NotImplementedError

    def insert_equipment(self, equipment, user_id):
        raise NotImplementedError

    def update_equipment(self, equipment, user_id):
        raise NotImplementedError

    def delete_equipment(self, equipment_id, user_id):
        raise NotImplementedError

    def insert_department(self, department, user_id):
        raise NotImplementedError

    def update_department(self, department, user_id):
        raise NotImplementedError

    def delete_department(self, department_id, updated_by, user_id):
        raise NotImplementedError

    def insert_equipment_class(self, equipment_class, user_id):
        raise NotImplementedError

    def update_workstation_sort_order(self, sort_orders, user_id):
        raise NotImplementedError

    def bulk_upload_machines(self, json_payload, clock_id, user_id):
        raise NotImplementedError
