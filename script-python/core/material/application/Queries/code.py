"""Query DTOs for read operations within the material module."""


class GetAllMaterialsQuery(object):
    def __init__(self, user_id):
        self.user_id = user_id


class GetMaterialRouteLinksQuery(object):
    def __init__(self, user_id, material_id):
        self.user_id = user_id
        self.material_id = material_id


class GetRoutesQuery(object):
    def __init__(self, user_id):
        self.user_id = user_id


class GetNcmTypesQuery(object):
    def __init__(self, user_id):
        self.user_id = user_id


class ExportMaterialsQuery(object):
    def __init__(self, user_id):
        self.user_id = user_id


class FilterBulkMaterialsQuery(object):
    def __init__(self, materials_data):
        self.materials_data = materials_data
