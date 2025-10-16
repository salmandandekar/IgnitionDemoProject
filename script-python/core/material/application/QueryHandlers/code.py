"""Application service layer for handling read operations."""


def handle_get_all_materials(query, repository, cache_port=None):
    cache_key = "materials:%s" % query.user_id
    if cache_port:
        cached = cache_port.get(cache_key)
        if cached is not None:
            return cached
    materials = repository.fetch_materials(query.user_id)
    if cache_port:
        try:
            cache_port.put(cache_key, materials, ttl_seconds=60)
        except Exception:
            pass
    return materials


def handle_get_material_route_links(query, repository):
    return repository.fetch_material_route_links(query.material_id, query.user_id)


def handle_get_routes(query, repository):
    return repository.fetch_routes(query.user_id)


def handle_get_ncm_types(query, repository):
    return repository.fetch_ncm_types(query.user_id)


def handle_export_materials(query, repository, cache_port=None):
    materials = handle_get_all_materials(query, repository, cache_port)
    headers = [
        "SAPMaterialID",
        "MaterialName",
        "Description",
        "IdleCycleTime(min)",
        "NCMType",
        "BaseQuantity",
        "RouteNumber",
        "Action",
    ]
    data = []
    for item in materials or []:
        source = item if isinstance(item, dict) else getattr(item, "to_record", lambda: item)()
        row = [
            source.get("MaterialName") or source.get("Name"),
            source.get("MaterialDescription") or source.get("Description"),
            source.get("MaterialDescription"),
            source.get("IdealCycleTime"),
            source.get("NCM"),
            float(source.get("BaseQuantity") or 0),
            source.get("DefaultRoute"),
            "I",
        ]
        data.append(row)
    return {"headers": headers, "data": data}


def handle_filter_bulk_materials(query):
    return [row for row in query.materials_data if row.get("Flag") == 0]
