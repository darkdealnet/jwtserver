from typing import List, Optional
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
import jwtserver.models as models
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


# class UserMarshSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = models.User
#         include_fk = True
#         load_instance = True
#         exclude = ('password',)


class UserFullPD(UserPD):
    password: str

    class Config:
        orm_mode = True
