"""Repository adapter bridging the material aggregate with stored procedures."""

import json

from common.cache.CacheManager import code as cache
from common.exceptions import RepositoryException as rex
from common.logging.LogFactory import code as LogFactory
from core.material.domain.Entities import code as EntitiesModule

Material = EntitiesModule.Material
MaterialRouteLink = EntitiesModule.MaterialRouteLink
Route = EntitiesModule.Route
NcmType = EntitiesModule.NcmType

_LOG = LogFactory.get_logger("MaterialRepository")
_CACHE_BUCKET = "material"
_DS_CACHE_PREFIX = "datasource"

SP_GET_MATERIALS = "usp_S_GetMaterial"
SP_INSERT_MATERIAL = "usp_I_InsertMaterial"
SP_UPDATE_MATERIAL = "usp_U_UpdateMaterial"
SP_DELETE_MATERIAL = "usp_D_DeleteMaterial"
SP_GET_ROUTE_LINKS = "usp_S_GetMaterialRouteLink"
SP_GET_ROUTES = "usp_S_GetRoutes"
SP_INSERT_ROUTE_LINK = "usp_C_InsertMaterialRouteLink"
SP_UPDATE_DEFAULT_ROUTE = "usp_U_UpdateMaterialDefaultRoute"
SP_DELETE_ROUTE_LINK = "usp_D_DeleteMaterialRouteLink"
SP_GET_NCM_TYPES = "usp_S_GetNCMTypes"
SP_BULK_UPLOAD = "usp_C_BulkUploadMaterials"


def _resolve_datasource(user_id):
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


def _run_query(statement, params, datasource):
    try:
        from system.db import runPrepQuery

        if datasource:
            return runPrepQuery(statement, params, datasource)
        return runPrepQuery(statement, params)
    except Exception:
        # outside Ignition we just simulate empty set
        return []


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
            rows.append(dataset)
    return rows


def _first_row(dataset):
    rows = _dataset_to_dicts(dataset)
    return rows[0] if rows else {}


def fetch_materials(user_id):
    ds = _resolve_datasource(user_id)
    statement = "EXEC %s" % SP_GET_MATERIALS
    rows = _dataset_to_dicts(_run_query(statement, [], ds))
    materials = []
    for row in rows:
        try:
            materials.append(Material.from_record(row))
        except Exception as exc:
            _LOG.error("Failed to hydrate material: %s" % exc)
    return materials


def insert_material(material, user_id):
    ds = _resolve_datasource(user_id)
    record = material.to_record()
    params = [
        ("@Name", record.get("Name")),
        ("@Description", record.get("Description")),
        ("@Category", record.get("Category")),
        ("@Picture", record.get("Picture")),
        ("@SNFormula", record.get("SNFormula")),
        ("@SortOrder", record.get("SortOrder")),
        ("@StatusID", record.get("StatusID")),
        ("@MaterialGroupID", record.get("MaterialGroupID")),
        ("@UnitOfMeasureID", record.get("UnitofMeasureID")),
        ("@UnitOfMeasure1ID", record.get("UnitofMeasure1ID")),
        ("@JsonTag", json.dumps(record.get("JsonTag")) if record.get("JsonTag") else None),
        ("@IsDeleted", record.get("IsDeleted")),
        ("@UpdatedBy", record.get("UpdatedBy")),
        ("@IdealCycleTime", record.get("IdealCycleTime")),
        ("@NCMTypeID", record.get("NCMTypeID")),
        ("@BaseQuantity", record.get("BaseQuantity")),
        ("@MaterialDescription", record.get("MaterialDescription")),
    ]
    statement = "EXEC %s %s" % (
        SP_INSERT_MATERIAL,
        ", ".join(["%s=?" % name for name, _ in params]),
    )
    result = _first_row(_run_query(statement, [value for _, value in params], ds))
    message = result.get("OutputMessage")
    if message and message not in ("[[STPSuccessfullyAdded]]", "[[STPSuccess]]"):
        raise rex.RepositoryException(message)
    return result


def update_material(material, user_id):
    ds = _resolve_datasource(user_id)
    record = material.to_record()
    params = [
        ("@ID", record.get("ID")),
        ("@Name", record.get("Name")),
        ("@Description", record.get("Description")),
        ("@Category", record.get("Category")),
        ("@Picture", record.get("Picture")),
        ("@SNFormula", record.get("SNFormula")),
        ("@SortOrder", record.get("SortOrder")),
        ("@StatusID", record.get("StatusID")),
        ("@MaterialGroupID", record.get("MaterialGroupID")),
        ("@UnitOfMeasureID", record.get("UnitofMeasureID")),
        ("@UnitOfMeasure1ID", record.get("UnitofMeasure1ID")),
        ("@JsonTag", json.dumps(record.get("JsonTag")) if record.get("JsonTag") else None),
        ("@IsDeleted", record.get("IsDeleted")),
        ("@UpdatedBy", record.get("UpdatedBy")),
        ("@IdealCycleTime", record.get("IdealCycleTime")),
        ("@NCMTypeID", record.get("NCMTypeID")),
        ("@BaseQuantity", record.get("BaseQuantity")),
        ("@MaterialDescription", record.get("MaterialDescription")),
    ]
    statement = "EXEC %s %s" % (
        SP_UPDATE_MATERIAL,
        ", ".join(["%s=?" % name for name, _ in params]),
    )
    result = _first_row(_run_query(statement, [value for _, value in params], ds))
    message = result.get("OutputMessage")
    if message and message not in ("[[STPSuccessfullyUpdated]]", "[[STPSuccess]]"):
        raise rex.RepositoryException(message)
    return result


def delete_material(material_id, updated_by, user_id):
    ds = _resolve_datasource(user_id)
    params = [
        ("@MaterialID", material_id),
        ("@UpdatedBy", updated_by),
    ]
    statement = "EXEC %s %s" % (
        SP_DELETE_MATERIAL,
        ", ".join(["%s=?" % name for name, _ in params]),
    )
    return _first_row(_run_query(statement, [value for _, value in params], ds))


def fetch_material_route_links(material_id, user_id):
    ds = _resolve_datasource(user_id)
    params = [("@MaterialID", material_id)]
    statement = "EXEC %s %s" % (
        SP_GET_ROUTE_LINKS,
        ", ".join(["%s=?" % name for name, _ in params]),
    )
    rows = _dataset_to_dicts(_run_query(statement, [value for _, value in params], ds))
    return [MaterialRouteLink.from_record(row) for row in rows]


def fetch_routes(user_id):
    ds = _resolve_datasource(user_id)
    rows = _dataset_to_dicts(_run_query("EXEC %s" % SP_GET_ROUTES, [], ds))
    return [Route.from_record(row) for row in rows]


def insert_route_link(route_dataset, material_id, user_id):
    ds = _resolve_datasource(user_id)
    params = [
        ("@RouteData", route_dataset),
        ("@MaterialID", material_id),
    ]
    statement = "EXEC %s %s" % (
        SP_INSERT_ROUTE_LINK,
        ", ".join(["%s=?" % name for name, _ in params]),
    )
    return _first_row(_run_query(statement, [value for _, value in params], ds))


def update_default_route(material_id, route_id, is_secondary, user_id):
    ds = _resolve_datasource(user_id)
    params = [
        ("@MaterialID", material_id),
        ("@RouteID", route_id),
        ("@IsSecondary", is_secondary),
    ]
    statement = "EXEC %s %s" % (
        SP_UPDATE_DEFAULT_ROUTE,
        ", ".join(["%s=?" % name for name, _ in params]),
    )
    return _first_row(_run_query(statement, [value for _, value in params], ds))


def delete_route_link(material_id, route_id, user_id):
    ds = _resolve_datasource(user_id)
    params = [
        ("@MaterialID", material_id),
        ("@RouteID", route_id),
    ]
    statement = "EXEC %s %s" % (
        SP_DELETE_ROUTE_LINK,
        ", ".join(["%s=?" % name for name, _ in params]),
    )
    return _first_row(_run_query(statement, [value for _, value in params], ds))


def fetch_ncm_types(user_id):
    ds = _resolve_datasource(user_id)
    rows = _dataset_to_dicts(_run_query("EXEC %s" % SP_GET_NCM_TYPES, [], ds))
    return [NcmType.from_record(row) for row in rows]


def bulk_upload_materials(json_materials, clock_id, user_id):
    ds = _resolve_datasource(user_id)
    params = [
        ("@JsonMaterialsList", json_materials),
        ("@ClockID", clock_id),
    ]
    statement = "EXEC %s %s" % (
        SP_BULK_UPLOAD,
        ", ".join(["%s=?" % name for name, _ in params]),
    )
    return _first_row(_run_query(statement, [value for _, value in params], ds))
