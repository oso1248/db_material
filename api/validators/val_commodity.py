from .classes.cls_commodity import CommodityName, Sap, Inventory, Type
from pydantic import BaseModel, conint, constr
from . val_suppliers import SupplierInclude
from .classes.cls_universial import Note
from .val_users import UserInclude
from typing import Optional
from datetime import date


class CommodityInclude(BaseModel):
    id: int
    name_local: CommodityName
    name_bit: constr(min_length=5, max_length=50)
    name_common: CommodityName
    per_unit: conint(ge=0, le=1000)
    unit_of_measurement: str

    class Config:
        orm_mode = True



class CommodityBase(BaseModel):
    name_local: CommodityName
    name_bit: constr(min_length=5, max_length=50)
    name_common: CommodityName
    inventory: Inventory
    type: Type
    sap: Sap
    unit_of_measurement: str
    per_unit: conint(ge=0, le=1000)
    per_pallet: conint(ge=0, le=1000)
    note: Optional[Note]
    is_active: bool


class CommodityCreate(CommodityBase):
    is_active: Optional[bool]
    id_supplier: int


class CommodityGet(CommodityBase):
    id: int
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    supplier: SupplierInclude

    class Config:
        orm_mode = True


class CommodityUpdate(CommodityBase):
    is_active: bool
    id_supplier: int
