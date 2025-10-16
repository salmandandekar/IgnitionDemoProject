"""Command DTOs for write operations within the material module."""

from core.material.domain.DomainServices import code as DomainServicesModule


class CreateMaterialCommand(object):
    def __init__(self, user_id, payload):
        self.user_id = user_id
        self.material = DomainServicesModule.MaterialFactory.from_dict(payload)


class UpdateMaterialCommand(object):
    def __init__(self, user_id, payload):
        self.user_id = user_id
        self.material = DomainServicesModule.MaterialFactory.from_dict(payload)


class DeleteMaterialCommand(object):
    def __init__(self, user_id, material_id, updated_by):
        self.user_id = user_id
        self.material_id = material_id
        self.updated_by = updated_by


class InsertMaterialRouteLinkCommand(object):
    def __init__(self, user_id, route_dataset, material_id):
        self.user_id = user_id
        self.route_dataset = route_dataset
        self.material_id = material_id


class UpdateDefaultRouteCommand(object):
    def __init__(self, user_id, material_id, route_id, is_secondary=0):
        self.user_id = user_id
        self.material_id = material_id
        self.route_id = route_id
        self.is_secondary = is_secondary


class DeleteMaterialRouteLinkCommand(object):
    def __init__(self, user_id, material_id, route_id):
        self.user_id = user_id
        self.material_id = material_id
        self.route_id = route_id


class BulkUploadMaterialsCommand(object):
    def __init__(self, user_id, json_materials, clock_id):
        self.user_id = user_id
        self.json_materials = json_materials
        self.clock_id = clock_id
