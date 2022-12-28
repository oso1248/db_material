from .classes.cls_jobs import JobName, JobArea
from ..validators.val_users import UserInclude
from .classes.cls_universial import Note
from pydantic import BaseModel, conint
from datetime import datetime, date
from typing import Optional, List
from pydantic import Extra


class JobsBase(BaseModel):
    name_job: JobName
    name_area: JobArea
    job_order: Optional[conint(ge=1)]
    note: Optional[Note]

    class Config:
        orm_mode = True


class JobCreate(JobsBase):
    pass

    class Config:
        extra = Extra.allow


class JobsGet(JobsBase):
    id: int
    is_active: bool
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude

    class Config:
        orm_mode = True


class JobsUpdate(JobsBase):
    pass

    class Config:
        extra = Extra.allow


class JobsOrderListGet(BaseModel):
    name_job: JobName
    name_area: JobArea
    job_order: Optional[conint(ge=1)]

    class Config:
        orm_mode = True


class JobsOrderListUpdate(BaseModel):
    name_job: JobName
    name_area: JobArea
    job_order: conint(ge=1)

    class Config:
        extra = Extra.allow