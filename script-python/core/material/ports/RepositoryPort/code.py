"""Hexagonal port describing persistence operations for Material aggregates."""


class MaterialRepositoryPort(object):
    def fetch_materials(self, user_id):
        raise NotImplementedError

    def fetch_material_route_links(self, material_id, user_id):
        raise NotImplementedError

    def fetch_routes(self, user_id):
        raise NotImplementedError

    def fetch_ncm_types(self, user_id):
        raise NotImplementedError

    def insert_material(self, material, user_id):
        raise NotImplementedError

    def update_material(self, material, user_id):
        raise NotImplementedError

    def delete_material(self, material_id, updated_by, user_id):
        raise NotImplementedError

    def insert_route_link(self, route_dataset, material_id, user_id):
        raise NotImplementedError

    def update_default_route(self, material_id, route_id, is_secondary, user_id):
        raise NotImplementedError

    def delete_route_link(self, material_id, route_id, user_id):
        raise NotImplementedError

    def bulk_upload_materials(self, json_materials, clock_id, user_id):
        raise NotImplementedError
