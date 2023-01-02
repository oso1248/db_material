from ..validators.val_users import Password, Name
from pydantic import BaseModel, conint, EmailStr
from typing import  Optional


class UserLogin(BaseModel):
    eid: str
    password: str


class UserCurrent(BaseModel):
    id: int
    eid: str
    name_first: str
    permissions: conint(ge=0, le=6)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int
    

class ResetPassword(BaseModel):
    temporary_password: str
    email: bool

    class Config:
        orm_mode = True


class ResetEmail(BaseModel):
    email: Optional[EmailStr]


class ChangePassword(BaseModel):
    username: Name
    oldpassword: Password
    newpassword: Password
