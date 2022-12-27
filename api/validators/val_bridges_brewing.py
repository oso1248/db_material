from typing import Optional
from pydantic import BaseModel, confloat
from datetime import date
from .classes.cls_universial import Note
from .val_users import UserInclude
from .val_commodity import CommodityInclude
from .val_brands import BrewingBrandInclude
from pydantic import Extra


# Bridge Addition
class BridgeAdditionBase(BaseModel):
    id_brand_brewing: int
    id_commodity: int
    per_brew: confloat(ge=0, le=10000)
    note: Optional[Note]

    class Config:
        orm_mode = True


class BridgeAdditionCreate(BridgeAdditionBase):
    pass

    class Config:
        extra = Extra.allow


class BridgeAdditionGet(BridgeAdditionBase):
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    brand: BrewingBrandInclude
    commodity: CommodityInclude

    class Config:
        orm_mode = True


class BridgeAdditionUpdate(BridgeAdditionBase):
    pass

    class Config:
        extra = Extra.allow


class BridgeAdditionUpdateGet(BridgeAdditionBase):
    per_brew: Optional[confloat(ge=0, le=10000)]
    name_brand: str
    name_local: str

    class Config:
        orm_mode = True


# Bridge Kettle Hop
class BridgeKettleHopBase(BaseModel):
    id_brand_brewing: int
    id_commodity: int
    per_brew: confloat(ge=0, le=10000)
    note: Optional[Note]

    class Config:
        orm_mode = True


class BridgeKettleHopCreate(BridgeKettleHopBase):
    pass

    class Config:
        extra = Extra.allow


class BridgeKettleHopGet(BridgeKettleHopBase):
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    brand: BrewingBrandInclude
    commodity: CommodityInclude


    class Config:
        orm_mode = True


class BridgeKettleHopUpdate(BridgeKettleHopBase):
    pass

    class Config:
        extra = Extra.allow


class BridgeKettleHopUpdateGet(BridgeKettleHopBase):
    per_brew: Optional[confloat(ge=0, le=10000)]
    name_brand: str
    name_local: str

    class Config:
        orm_mode = True


# Bridge Kettle Hop
class BridgeDryHopBase(BaseModel):
    id_brand_brewing: int
    id_commodity: int
    per_brew: confloat(ge=0, le=10000)
    note: Optional[Note]

    class Config:
        orm_mode = True


class BridgeDryHopCreate(BridgeDryHopBase):
    pass

    class Config:
        extra = Extra.allow


class BridgeDryHopGet(BridgeDryHopBase):
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    brand: BrewingBrandInclude
    commodity: CommodityInclude

    class Config:
        orm_mode = True


class BridgeDryHopUpdate(BridgeDryHopBase):
    pass

    class Config:
        extra = Extra.allow


class BridgeDryHopUpdateGet(BridgeDryHopBase):
    per_brew: Optional[confloat(ge=0, le=10000)]
    name_brand: str
    name_local: str

    class Config:
        orm_mode = True
