from .classes.cls_universial import Note
from pydantic import BaseModel, constr
from datetime import datetime
from typing import Optional
from typing import List


class IssuesCreate(BaseModel):
    title: constr(min_length=5, max_length=32)
    body: Note
    labels: List[constr(regex='(bug|design|enhancement|question)$')]


class IssuesCreateGet(BaseModel):
    title: constr(min_length=5, max_length=32)
    body: constr(min_length=5, max_length=300)
    owner: constr(min_length=5, max_length=32)
    label: constr(regex='(bug|design|enhancement|question)$')
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    state: str
    id: int
    url: str

    class Config:
        orm_mode = True
