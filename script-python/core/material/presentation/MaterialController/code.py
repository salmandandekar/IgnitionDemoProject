"""Material controller exposing application layer to Ignition scripts."""

from common.logging.LogFactory import code as LogFactory
from core.material.application.Commands import code as cmds
from core.material.application.CommandHandlers import code as ch
from core.material.application.Queries import code as queries
from core.material.application.QueryHandlers import code as qh
from core.material.domain.DomainServices import code as DomainServicesModule
from core.material.infrastructure.RepositoryAdapter import code as repo
from core.material.infrastructure.CacheAdapter import code as cache
from core.material.infrastructure.MessagingAdapter import code as messaging

_LOG = LogFactory.get_logger("MaterialController")


class MaterialController(object):
    def __init__(self, user_id, repository=None, cache_port=None, messenger=None):
        self.user_id = user_id
        self.repository = repository or _RepositoryAdapter()
        self.cache_port = cache_port or _CachePort()
        self.messenger = messenger or messaging.get_messenger()

    def get_materials(self):
        try:
            q = queries.GetAllMaterialsQuery(self.user_id)
            return qh.handle_get_all_materials(q, self.repository, self.cache_port)
        except Exception as exc:
            _LOG.error("Failed to get materials: %s" % exc)
            raise

    def create_material(self, payload):
        command = cmds.CreateMaterialCommand(self.user_id, payload)
        return ch.handle_create_material(command, self.repository, self.cache_port, self.messenger)

    def update_material(self, payload):
        command = cmds.UpdateMaterialCommand(self.user_id, payload)
        return ch.handle_update_material(command, self.repository, self.cache_port, self.messenger)

    def delete_material(self, material_id, updated_by):
        command = cmds.DeleteMaterialCommand(self.user_id, material_id, updated_by)
        return ch.handle_delete_material(command, self.repository, self.cache_port, self.messenger)

    def get_material_route_links(self, material_id):
        q = queries.GetMaterialRouteLinksQuery(self.user_id, material_id)
        return qh.handle_get_material_route_links(q, self.repository)

    def get_routes(self):
        q = queries.GetRoutesQuery(self.user_id)
        return qh.handle_get_routes(q, self.repository)

    def insert_material_route_link(self, route_dataset, material_id):
        command = cmds.InsertMaterialRouteLinkCommand(self.user_id, route_dataset, material_id)
        return ch.handle_insert_route_link(command, self.repository, self.messenger)

    def update_default_route(self, material_id, route_id, is_secondary=0):
        command = cmds.UpdateDefaultRouteCommand(self.user_id, material_id, route_id, is_secondary)
        return ch.handle_update_default_route(command, self.repository, self.messenger)

    def delete_material_route_link(self, material_id, route_id):
        command = cmds.DeleteMaterialRouteLinkCommand(self.user_id, material_id, route_id)
        return ch.handle_delete_route_link(command, self.repository, self.messenger)

    def get_ncm_types(self):
        q = queries.GetNcmTypesQuery(self.user_id)
        return qh.handle_get_ncm_types(q, self.repository)

    def bulk_upload_materials(self, json_materials, clock_id):
        command = cmds.BulkUploadMaterialsCommand(self.user_id, json_materials, clock_id)
        return ch.handle_bulk_upload_materials(command, self.repository, self.messenger)

    def export_materials(self):
        q = queries.ExportMaterialsQuery(self.user_id)
        return qh.handle_export_materials(q, self.repository, self.cache_port)

    def filter_valid_materials(self, materials_data):
        q = queries.FilterBulkMaterialsQuery(materials_data)
        return qh.handle_filter_bulk_materials(q)

    def validate_bulk_material_rows(self, rows, existing_materials=None, ncm_types=None, routes=None, work_orders=None):
        service = DomainServicesModule.BulkMaterialValidationService(existing_materials, ncm_types, routes, work_orders)
        return service.validate(rows)


class _RepositoryAdapter(object):
    def fetch_materials(self, user_id):
        return repo.fetch_materials(user_id)

    def fetch_material_route_links(self, material_id, user_id):
        return repo.fetch_material_route_links(material_id, user_id)

    def fetch_routes(self, user_id):
        return repo.fetch_routes(user_id)

    def fetch_ncm_types(self, user_id):
        return repo.fetch_ncm_types(user_id)

    def insert_material(self, material, user_id):
        return repo.insert_material(material, user_id)

    def update_material(self, material, user_id):
        return repo.update_material(material, user_id)

    def delete_material(self, material_id, updated_by, user_id):
        return repo.delete_material(material_id, updated_by, user_id)

    def insert_route_link(self, route_dataset, material_id, user_id):
        return repo.insert_route_link(route_dataset, material_id, user_id)

    def update_default_route(self, material_id, route_id, is_secondary, user_id):
        return repo.update_default_route(material_id, route_id, is_secondary, user_id)

    def delete_route_link(self, material_id, route_id, user_id):
        return repo.delete_route_link(material_id, route_id, user_id)

    def bulk_upload_materials(self, json_materials, clock_id, user_id):
        return repo.bulk_upload_materials(json_materials, clock_id, user_id)


class _CachePort(object):
    def get(self, key):
        return cache.get(key)

    def put(self, key, value, ttl_seconds=60):
        return cache.put(key, value, ttl_seconds)

    def invalidate(self, key=None):
        return cache.invalidate(key)
