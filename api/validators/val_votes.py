from pydantic import BaseModel, conint


class VoteBase(BaseModel):
    id_post: int
    dir: conint(ge=0, le=1)
