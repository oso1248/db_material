from .classes.cls_universial import PhoneNumber
from .classes.cls_suppliers import SupplierName
from pydantic import BaseModel, EmailStr
from .val_users import UserInclude
from typing import Optional
from datetime import date


class SupplierInclude(BaseModel):
    id: int
    name_supplier: SupplierName
    name_contact: SupplierName
    phone: PhoneNumber
    email: EmailStr

    class Config:
        orm_mode = True


class SupplierBase(BaseModel):
    name_supplier: SupplierName
    is_active: bool
    name_contact: SupplierName
    phone: PhoneNumber
    email: EmailStr
    note: Optional[str] = None


class SupplierCreate(SupplierBase):
    is_active: Optional[bool]


class SupplierGet(SupplierBase):
    id: int
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude

    class Config:
        orm_mode = True


class SupplierUpdate(SupplierBase):
    is_active: bool
