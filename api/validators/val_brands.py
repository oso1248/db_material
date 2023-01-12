from ..validators.val_users import UserInclude
from .classes.cls_brands import BrandName
from .classes.cls_universial import Note
from typing import Optional, List
from pydantic import BaseModel
from datetime import date


# Include Brands
class BrewingBrandInclude(BaseModel):
    id: int
    name_brand: BrandName
    is_active: bool
    is_organic: bool
    note: Optional[Note]

    class Config:
        orm_mode = True


class FinishingBrandInclude(BaseModel):
    id: int
    name_brand: BrandName
    note: Optional[Note]

    class Config:
        orm_mode = True


class PackagingBrandInclude(BaseModel):
    id: int
    name_brand: BrandName
    note: Optional[Note]

    class Config:
        orm_mode = True


# Brewing Brand
class BrewingBrandBase(BaseModel):
    name_brand: BrandName
    is_active: bool
    is_organic: bool
    note: Optional[Note] = None


class BrewingBrandCreate(BrewingBrandBase):
    is_active: Optional[bool] = True
    is_organic: Optional[bool] = False
    is_dryhop: Optional[bool] = False
    is_addition: Optional[bool] = False


class BrewingBrandGet(BrewingBrandBase):
    id: int
    is_dryhop: bool
    is_addition: bool
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    children: List[FinishingBrandInclude]
    grandchildren: List[PackagingBrandInclude]

    class Config:
        orm_mode = True


class BrewingBrandUpdate(BaseModel):
    name_brand: BrandName
    is_active: bool
    is_organic: bool
    is_dryhop: bool
    is_addition: bool
    note: Optional[Note] = None


# Finishing Brand
class FinishingBrandBase(BaseModel):
    name_brand: BrandName
    is_preinjection: bool
    is_postinjection: bool
    note: Optional[Note] = None


class FinishingBrandCreate(FinishingBrandBase):
    id_brand_brewing: int
    is_preinjection: Optional[bool] = False
    is_postinjection: Optional[bool] = False


class FinishingBrandGet(FinishingBrandBase):
    id: int
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    parent: BrewingBrandInclude
    children: List[PackagingBrandInclude]

    class Config:
        orm_mode = True


class FinishingBrandUpdate(BaseModel):
    id_brand_brewing: int
    name_brand: BrandName
    is_preinjection: bool
    is_postinjection: bool
    note: Optional[Note] = None


# Packaging Brand
class PackagingBrandBase(BaseModel):
    name_brand: BrandName
    note: Optional[Note] = None


class PackagingBrandCreate(PackagingBrandBase):
    id_brand_finishing: int


class PackagingBrandGet(PackagingBrandBase):
    id: int
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    parent: FinishingBrandInclude
    grandparent: List[BrewingBrandInclude]

    class Config:
        orm_mode = True


class PackagingBrandUpdate(BaseModel):
    id_brand_finishing: int
    name_brand: BrandName
    note: Optional[Note] = None
