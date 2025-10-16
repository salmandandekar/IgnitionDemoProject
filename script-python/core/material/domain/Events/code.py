"""Domain events emitted by the Material aggregate."""

class MaterialCreated(object):
    def __init__(self, material_id, name):
        self.material_id = material_id
        self.name = name


class MaterialUpdated(object):
    def __init__(self, material_id, name):
        self.material_id = material_id
        self.name = name


class MaterialDeleted(object):
    def __init__(self, material_id, deleted_by):
        self.material_id = material_id
        self.deleted_by = deleted_by


class MaterialRoutesLinked(object):
    def __init__(self, material_id, route_ids):
        self.material_id = material_id
        self.route_ids = route_ids or []


class MaterialsBulkImported(object):
    def __init__(self, imported_count, failed_count):
        self.imported_count = imported_count
        self.failed_count = failed_count
