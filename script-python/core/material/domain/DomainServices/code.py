"""Domain services encapsulating business rules for materials."""

from core.material.domain.Entities import code as EntitiesModule


class MaterialFactory(object):
    """Factory that safeguards creation of Material aggregates."""

    REQUIRED_DEFAULTS = {
        "Category": 1,
        "SortOrder": 1,
        "StatusID": 1,
        "MaterialGroupID": 1,
        "UnitofMeasureID": 1,
        "UnitofMeasure1ID": 1,
        "IsDeleted": 0,
    }

    @staticmethod
    def from_dict(payload):
        data = dict(MaterialFactory.REQUIRED_DEFAULTS)
        data.update(payload or {})
        return EntitiesModule.Material(
            material_id=data.get("ID") or data.get("MaterialID"),
            row_id=data.get("RowID"),
            row_version=data.get("RowVersion"),
            name=data.get("Name") or data.get("MaterialName"),
            description=data.get("Description"),
            material_description=data.get("MaterialDescription"),
            category=data.get("Category"),
            picture=data.get("Picture"),
            sn_formula=data.get("SNFormula"),
            sort_order=data.get("SortOrder"),
            status_id=data.get("StatusID"),
            material_group_id=data.get("MaterialGroupID"),
            uom_id=data.get("UnitofMeasureID"),
            secondary_uom_id=data.get("UnitofMeasure1ID"),
            json_tag=data.get("JsonTag"),
            is_deleted=data.get("IsDeleted"),
            insert_time=data.get("InsertTime"),
            update_time=data.get("UpdateTime"),
            updated_by=data.get("UpdatedBy"),
            ideal_cycle_time=data.get("IdealCycleTime"),
            target_cycle_time=data.get("TargetCycleTime"),
            hourly_target=data.get("HourlyTarget"),
            ncm_type_id=data.get("NCMTypeID"),
            base_quantity=data.get("BaseQuantity"),
            ncm=data.get("NCM"),
            default_route=data.get("DefaultRoute"),
        )


class BulkMaterialValidationService(object):
    """Executes domain validation rules for bulk material import rows."""

    def __init__(self, existing_materials=None, ncm_types=None, routes=None, work_orders=None):
        self._materials_by_sap = {}
        for material in existing_materials or []:
            key = getattr(material, "material_name", None) or getattr(material, "name", None)
            if not key:
                key = material.material_id.value if hasattr(material, "material_id") else None
            if isinstance(material, dict):
                key = material.get("MaterialName") or material.get("Name")
            if key:
                self._materials_by_sap[str(key)] = material

        self._ncm_lookup = {}
        for item in ncm_types or []:
            if isinstance(item, dict):
                label = item.get("label") or item.get("NCMTypeDescription")
                value = item.get("value") or item.get("NCMTypeID")
            else:
                label = getattr(item, "description", None)
                value = getattr(item, "ncm_type_id", None)
            if label:
                self._ncm_lookup[str(label)] = value

        self._routes_lookup = set()
        for route in routes or []:
            if isinstance(route, dict):
                number = route.get("RouteNumber") or route.get("routeNumber")
            else:
                number = getattr(route, "route_number", None)
            if number:
                self._routes_lookup.add(str(number))

        self._materials_in_work_orders = set()
        for wo in work_orders or []:
            if isinstance(wo, dict):
                mid = wo.get("MaterialID")
            else:
                mid = getattr(wo, "material_id", None)
            if mid:
                self._materials_in_work_orders.add(str(mid))

    def validate(self, rows):
        processed = []
        duplicates = self._detect_duplicates(rows)

        for raw in rows:
            bulk_row = EntitiesModule.BulkMaterialRow(raw)
            if not bulk_row.sap_material_id:
                continue  # skip empty rows silently

            if bulk_row.sap_material_id in duplicates:
                bulk_row.add_error("Same SAPMaterialID present multiple times")

            action = bulk_row.action or "I"
            material_ref = self._materials_by_sap.get(bulk_row.sap_material_id)

            if action == "I":
                if material_ref:
                    has_route = False
                    if isinstance(material_ref, dict):
                        has_route = bool(material_ref.get("DefaultRoute"))
                        material_id = material_ref.get("ID")
                    else:
                        has_route = getattr(material_ref, "default_route", None) not in (None, "")
                        material_id = getattr(material_ref.material_id, "value", None)
                    if bulk_row.route_number and has_route:
                        bulk_row.add_error("SAPMaterialID with given Route Already exists")
                    else:
                        bulk_row.add_error("SAPMaterialID Already exists")
            elif action in ("U", "D"):
                if not material_ref:
                    bulk_row.add_error("SAPMaterialID does not exists")

            if not bulk_row.material_name:
                bulk_row.add_error("Please Enter Material Name")

            try:
                if float(bulk_row.ideal_cycle_time) <= 0:
                    bulk_row.add_error("Idle Cycle Time must be greater than 0")
            except Exception:
                bulk_row.add_error("Idle Cycle Time must be greater than 0")

            ncm_type_id = self._ncm_lookup.get(bulk_row.ncm_type)
            if not ncm_type_id:
                bulk_row.add_error("Please Enter Valid NCM")
            raw.update({"NCMTypeID": ncm_type_id})

            base_qty_raw = raw.get("BaseQuantity")
            try:
                base_qty = float(str(base_qty_raw).replace(",", ""))
            except Exception:
                base_qty = -1
            if base_qty <= 0:
                bulk_row.add_error("BaseQuantity must be greater than 0")
            raw["BaseQuantity"] = base_qty

            if bulk_row.route_number and bulk_row.route_number not in self._routes_lookup:
                bulk_row.add_error("Please Enter Valid Route Number")

            if action not in ("I", "U", "D"):
                bulk_row.add_error("Please Enter Valid Action(I/U/D)")

            if action == "D" and material_ref:
                material_id = None
                if isinstance(material_ref, dict):
                    material_id = material_ref.get("ID") or material_ref.get("MaterialID")
                else:
                    material_id = getattr(material_ref.material_id, "value", None)
                if material_id and str(material_id) in self._materials_in_work_orders:
                    bulk_row.add_error("WorkOrder exists against material Cannot be Deleted")

            if bulk_row.is_valid():
                raw["Flag"] = 0
            else:
                raw["Flag"] = 1
            raw.update(bulk_row.to_feedback())
            processed.append(raw)
        return processed

    @staticmethod
    def _detect_duplicates(rows):
        seen = set()
        duplicates = set()
        for row in rows:
            sap = row.get("SAPMaterialID")
            if not sap:
                continue
            if sap in seen:
                duplicates.add(sap)
            else:
                seen.add(sap)
        return duplicates
