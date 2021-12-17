from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TokenPD(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenDataPD(BaseModel):
    uuid: Optional[UUID] = None

    class Config:
        orm_mode = True


class RegistrationDataPD(BaseModel):
    telephone: str
    password: str

    class Config:
        orm_mode = True


class UserPD(BaseModel):
    uuid: UUID
    telephone: str
    is_active: Optional[bool] = False
    is_admin: Optional[bool] = False

    class Config:
        orm_mode = True



class UserFullPD(UserPD):
    password: str

    class Config:
        orm_mode = True
