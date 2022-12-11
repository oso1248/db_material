from .classes.cls_users import Eid, Name, Password
from pydantic import BaseModel, conint
from datetime import datetime


class UsersBase(BaseModel):
    eid: Eid
    name_first: Name
    name_last: Name
    is_active: bool = True
    permissions: conint(ge=0, le=7) = 1


class UserInclude(BaseModel):
    name_first: str
    name_last: str

    class Config:
        orm_mode = True


class UsersCreate(UsersBase):
    password: Password


class UsersGet(UsersBase):
    id: int
    time_created: datetime
    creator: UserInclude
    updater: UserInclude

    class Config:
        orm_mode = True


class UsersUpdate(BaseModel):
    is_active: bool
    permissions: conint(ge=0, le=6)
