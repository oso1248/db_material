from typing import Optional
from pydantic import BaseModel, confloat, conint
from datetime import date
from .classes.cls_universial import Note
from .classes.cls_inventory import LastBrew, HopLot
from .val_users import UserInclude
from .val_commodity import CommodityInclude
from .val_brands import BrewingBrandInclude
from pydantic import Extra
from pydantic import UUID4


class InvRetrieve(BaseModel):
    uuid: UUID4


class InvDatesGet(BaseModel):
    inventory_date: date
    uuid: UUID4

    class Config:
        orm_mode = True


class InvUuidInclude(BaseModel):
    inventory_date: date
    uuid: UUID4

    class Config:
        orm_mode = True


class InvLastBrewsInclude(BaseModel):
    bh_1: LastBrew
    bh_2: LastBrew

    class Config:
        orm_mode = True


# Material
class InvMaterialBase(BaseModel):
    final_count: confloat(ge=0, le=100000000)
    final_total: confloat(ge=0, le=100000000)
    note: Optional[Note]

    class Config:
        orm_mode = True


class InvMaterialCreate(InvMaterialBase):
    id_commodity: int

    class Config:
        extra = Extra.allow


class InvMaterialGet(InvMaterialBase):
    id: int
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    commodity: CommodityInclude
    inventory: InvUuidInclude

    class Config:
        orm_mode = True


class InvMaterialUpdate(InvMaterialBase):
    pass


# Hop
class InvHopBase(BaseModel):
    final_boxes: confloat(ge=0, le=100000000)
    final_pounds: confloat(ge=0, le=100000000)
    final_total: confloat(ge=0, le=100000000)
    lot_number: HopLot
    is_current: bool
    note: Optional[Note]

    class Config:
        orm_mode = True


class InvHopCreate(InvHopBase):
    id_commodity: int

    class Config:
        extra = Extra.allow


class InvHopGet(InvHopBase):
    id: int
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    commodity: CommodityInclude
    last_brews: Optional[InvLastBrewsInclude]
    inventory: InvUuidInclude

    class Config:
        orm_mode = True


class InvHopUpdate(InvHopBase):
    pass


# Last Brews
class InvLastBrewsBase(BaseModel):
    bh_1: LastBrew
    bh_2: LastBrew
    note: Optional[Note]


class InvLastBrewsCreate(InvLastBrewsBase):
    pass


class InvLastBrewsGet(InvLastBrewsBase):
    id: int
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    inventory: InvUuidInclude

    class Config:
        orm_mode = True


class InvLastBrewsUpdate(InvLastBrewsBase):
    pass


# Hibernate
class InvHibernateBase(BaseModel):
    tank_origin: int
    tank_origin_level: conint(ge=0, le=5000)
    tank_storage: int
    tank_storage_level: conint(ge=0, le=5000)
    tank_storage_og: confloat(ge=0, le=50)
    tank_storage_abw: confloat(ge=0, le=50)
    tank_storage_o2: conint(ge=0, le=1000)
    note_origin: Optional[Note]

    class Config:
        orm_mode = True


class InvHibernateCreate(InvHibernateBase):
    id_brand_brewing: int


class InvHibernateGet(InvHibernateBase):
    id: int
    tank_final: Optional[int]
    tank_final_level: Optional[conint(ge=0, le=5000)]
    note_final: Optional[Note]
    is_complete: bool
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    brand: BrewingBrandInclude

    class Config:
        orm_mode = True


class InvHibernateUpdate(InvHibernateBase):
    id_brand_brewing: Optional[int]
    tank_final: Optional[int]
    tank_final_level: Optional[conint(ge=0, le=5000)]
    note_final: Optional[Note]
    is_complete: bool
