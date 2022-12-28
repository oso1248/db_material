from .classes.cls_jobs import JobName, JobArea
from ..validators.val_users import UserInclude
from .classes.cls_universial import Note
from pydantic import BaseModel, conint
from datetime import datetime, date
from typing import Optional, List
from pydantic import Extra


class JobInclude(BaseModel):
    name_job: JobName
    name_area: JobArea
    note: Optional[Note]

    class Config:
        orm_mode = True


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
    brewers: List[UserInclude]

    class Config:
        orm_mode = True


class JobsUpdate(JobsBase):
    pass

    class Config:
        extra = Extra.allow


class JobsOrderUpdateList(BaseModel):
    name_job: JobName
    name_area: JobArea
    job_order: Optional[conint(ge=1)]

    class Config:
        orm_mode = True
        # extra = Extra.allow


class UserJobsBase(BaseModel):
    id_user: conint(ge=1)
    id_jobs_brewing: conint(ge=1)
    skap: conint(ge=0, le=5)
    note: Optional[Note]

    class Config:
        orm_mode = True


class UserJobsCreate(UserJobsBase):
    pass


class UserJobsGet(UserJobsBase):
    brewer: UserInclude
    job: JobInclude
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude

    class Config:
        orm_mode = True


class UserJobsUpdateList(BaseModel):
    id_user: conint(ge=0)
    id_jobs_brewing: conint(ge=0)
    name_first: str
    name_job: JobName
    skap: conint(ge=0, le=5)

    class Config:
        orm_mode = True


class BridgeUserJobsGet(UserJobsBase):
    time_created: date
    time_updated: date
    creator: UserInclude
    updater: UserInclude
    brewer: UserInclude
    job: JobInclude

    class Config:
        orm_mode = True


class UserJobsUpdate(BaseModel):
    id_user: conint(ge=1)
    id_jobs_brewing: conint(ge=1)
    skap: conint(ge=0, le=5)
    note: Optional[Note]
