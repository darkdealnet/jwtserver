import uuid as _uuid
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils.types.phone_number import PhoneNumberType
from jwtserver.database import Base


class User(Base):

    __tablename__ = "users"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=_uuid.uuid4)
    telephone = Column(PhoneNumberType())
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def __repr__(self):
        return "<User('%s','%s')>" % (self.uuid, self.telephone)


class RefreshToken(Base):
    __tablename__ = "refresh_token"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
