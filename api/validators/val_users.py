from .classes.cls_users import Eid, Name, Password
from pydantic import BaseModel, conint
from datetime import date
from .classes.cls_jobs import JobName, JobArea
from .classes.cls_universial import Note
from typing import Optional, List


class Jobs(BaseModel):
    name_job: JobName
    name_area: JobArea
    note: Optional[Note]

    class Config:
        orm_mode = True


class UsersBase(BaseModel):
    eid: Eid
    name_first: Name
    name_last: Name
    is_active: bool = True
    permissions: conint(ge=0, le=7)


class UserInclude(BaseModel):
    name_first: str
    name_last: str

    class Config:
        orm_mode = True


class UsersCreate(UsersBase):
    permissions: conint(ge=0, le=6) = 1
    password: Password


class UsersGet(UsersBase):
    id: int
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    jobs: List[Jobs]

    class Config:
        orm_mode = True


class UsersUpdate(BaseModel):
    is_active: bool
    permissions: conint(ge=0, le=6)
