"""Aggregate roots and entities for the Material bounded context."""

from core.material.domain.ValueObjects import code as ValueObjectsModule

MaterialId = ValueObjectsModule.MaterialId
RouteId = ValueObjectsModule.RouteId
CycleTime = ValueObjectsModule.CycleTime
BaseQuantity = ValueObjectsModule.BaseQuantity
JsonTag = ValueObjectsModule.JsonTag


class Material(object):
    """Material aggregate root encapsulating all mutable state."""

    def __init__(
        self,
        material_id=None,
        row_id=None,
        row_version=None,
        name=None,
        description=None,
        material_description=None,
        category=None,
        picture=None,
        sn_formula=None,
        sort_order=None,
        status_id=None,
        material_group_id=None,
        uom_id=None,
        secondary_uom_id=None,
        json_tag=None,
        is_deleted=False,
        insert_time=None,
        update_time=None,
        updated_by=None,
        ideal_cycle_time=None,
        target_cycle_time=None,
        hourly_target=None,
        ncm_type_id=None,
        base_quantity=None,
        ncm=None,
        default_route=None,
    ):
        self.material_id = MaterialId(material_id)
        self.row_id = row_id
        self.row_version = row_version
        self.name = name
        self.description = description
        self.material_description = material_description
        self.category = category
        self.picture = picture
        self.sn_formula = sn_formula
        self.sort_order = sort_order
        self.status_id = status_id
        self.material_group_id = material_group_id
        self.uom_id = uom_id
        self.secondary_uom_id = secondary_uom_id
        self.json_tag = JsonTag(json_tag).value if not isinstance(json_tag, JsonTag) else json_tag.value
        self.is_deleted = bool(is_deleted)
        self.insert_time = insert_time
        self.update_time = update_time
        self.updated_by = updated_by
        self.ideal_cycle_time = CycleTime(ideal_cycle_time).as_minutes() if ideal_cycle_time not in (None, "") else None
        self.target_cycle_time = CycleTime(target_cycle_time).as_minutes() if target_cycle_time not in (None, "") else None
        self.hourly_target = hourly_target
        self.ncm_type_id = ncm_type_id
        if base_quantity in (None, ""):
            self.base_quantity = None
        else:
            self.base_quantity = BaseQuantity(base_quantity).as_float()
        self.ncm = ncm
        self.default_route = default_route
        self._validate()

    def _validate(self):
        if not self.name:
            raise ValueError("Material name is required")
        if self.base_quantity is not None and self.base_quantity <= 0:
            raise ValueError("Base quantity must be greater than zero")

    def identity(self):
        return self.material_id

    def mark_deleted(self, updated_by):
        self.is_deleted = True
        self.updated_by = updated_by

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if not hasattr(self, key):
                continue
            setattr(self, key, value)
        self._validate()

    def to_record(self):
        """Return dict representation for infrastructure mapping."""
        return {
            "ID": self.material_id.value,
            "RowID": self.row_id,
            "RowVersion": self.row_version,
            "Name": self.name,
            "Description": self.description,
            "MaterialDescription": self.material_description,
            "Category": self.category,
            "Picture": self.picture,
            "SNFormula": self.sn_formula,
            "SortOrder": self.sort_order,
            "StatusID": self.status_id,
            "MaterialGroupID": self.material_group_id,
            "UnitofMeasureID": self.uom_id,
            "UnitofMeasure1ID": self.secondary_uom_id,
            "JsonTag": self.json_tag,
            "IsDeleted": int(self.is_deleted),
            "InsertTime": self.insert_time,
            "UpdateTime": self.update_time,
            "UpdatedBy": self.updated_by,
            "IdealCycleTime": self.ideal_cycle_time,
            "TargetCycleTime": self.target_cycle_time,
            "HourlyTarget": self.hourly_target,
            "NCMTypeID": self.ncm_type_id,
            "BaseQuantity": self.base_quantity,
            "NCM": self.ncm,
            "DefaultRoute": self.default_route,
        }

    @staticmethod
    def from_record(record):
        record = record or {}
        return Material(
            material_id=record.get("ID") or record.get("MaterialID") or record.get("MaterialId"),
            row_id=record.get("RowID"),
            row_version=record.get("RowVersion"),
            name=record.get("MaterialName") or record.get("Name"),
            description=record.get("Description"),
            material_description=record.get("MaterialDescription"),
            category=record.get("Category"),
            picture=record.get("Picture"),
            sn_formula=record.get("SNFormula"),
            sort_order=record.get("SortOrder"),
            status_id=record.get("StatusID"),
            material_group_id=record.get("MaterialGroupID"),
            uom_id=record.get("UnitofMeasureID"),
            secondary_uom_id=record.get("UnitofMeasure1ID"),
            json_tag=record.get("JsonTag"),
            is_deleted=record.get("IsDeleted", False),
            insert_time=record.get("InsertTime"),
            update_time=record.get("UpdateTime"),
            updated_by=record.get("UpdatedBy"),
            ideal_cycle_time=record.get("IdealCycleTime"),
            target_cycle_time=record.get("TargetCycleTime"),
            hourly_target=record.get("HourlyTarget"),
            ncm_type_id=record.get("NCMTypeID"),
            base_quantity=record.get("BaseQuantity"),
            ncm=record.get("NCM"),
            default_route=record.get("DefaultRoute"),
        )


class MaterialRouteLink(object):
    def __init__(
        self,
        material_id=None,
        route_id=None,
        route_name=None,
        description=None,
        status=None,
        is_default=False,
        route_number=None,
        revision=None,
        is_secondary=False,
    ):
        self.material_id = MaterialId(material_id)
        self.route_id = RouteId(route_id)
        self.route_name = route_name
        self.description = description
        self.status = status
        self.is_default = bool(is_default)
        self.route_number = route_number
        self.revision = revision
        self.is_secondary = bool(is_secondary)

    @staticmethod
    def from_record(record):
        record = record or {}
        return MaterialRouteLink(
            material_id=record.get("MaterialID"),
            route_id=record.get("RouteID"),
            route_name=record.get("RouteName"),
            description=record.get("Description"),
            status=record.get("Status"),
            is_default=record.get("IsDefault"),
            route_number=record.get("RouteNumber"),
            revision=record.get("Revision"),
            is_secondary=record.get("IsSecondary"),
        )

    def to_record(self):
        return {
            "MaterialID": self.material_id.value,
            "RouteID": self.route_id.value,
            "RouteName": self.route_name,
            "Description": self.description,
            "Status": self.status,
            "IsDefault": int(self.is_default),
            "RouteNumber": self.route_number,
            "Revision": self.revision,
            "IsSecondary": int(self.is_secondary),
        }


class Route(object):
    def __init__(self, route_id=None, route_name=None, description=None, status=None, label=None, value=None, route_number=None):
        self.route_id = RouteId(route_id)
        self.route_name = route_name
        self.description = description
        self.status = status
        self.label = label or route_name
        self.value = value or self.route_id.value
        self.route_number = route_number

    @staticmethod
    def from_record(record):
        record = record or {}
        return Route(
            route_id=record.get("RouteID"),
            route_name=record.get("RouteName"),
            description=record.get("Description"),
            status=record.get("Status"),
            label=record.get("label"),
            value=record.get("value"),
            route_number=record.get("RouteNumber"),
        )

    def to_record(self):
        return {
            "RouteID": self.route_id.value,
            "RouteName": self.route_name,
            "Description": self.description,
            "Status": self.status,
            "label": self.label,
            "value": self.value,
            "RouteNumber": self.route_number,
        }


class NcmType(object):
    def __init__(self, ncm_type_id=None, description=None):
        self.ncm_type_id = ncm_type_id
        self.description = description

    def to_choice(self):
        return {"label": self.description, "value": self.ncm_type_id}

    @staticmethod
    def from_record(record):
        record = record or {}
        return NcmType(record.get("NCMTypeID"), record.get("NCMTypeDescription"))


class BulkMaterialRow(object):
    """Represents a row in the bulk material import template."""

    def __init__(self, row_dict):
        self.raw = dict(row_dict)
        self.errors = []
        self.material_id = row_dict.get("MaterialID")
        self.sap_material_id = row_dict.get("SAPMaterialID")
        self.material_name = row_dict.get("MaterialName")
        self.description = row_dict.get("Description")
        self.ideal_cycle_time = row_dict.get("IdealCycleTime")
        self.ncm_type = row_dict.get("NCMType")
        self.route_number = row_dict.get("RouteNumber")
        self.action = (row_dict.get("Action") or "").upper()

    def add_error(self, message):
        self.errors.append(message)

    def is_valid(self):
        return len(self.errors) == 0

    def to_feedback(self):
        style = {}
        if self.errors:
            style = {"backgroundColor": "#FF474C", "font-weight": "bold", "color": "#FFFFFF"}
        return {
            "Flag": 0 if self.is_valid() else 1,
            "Reasons": {"value": ",".join(self.errors), "style": style},
        }
