from typing import Literal

from fastapi.param_functions import Optional, Cookie
from jose import JWTError, jwt
from pydantic import BaseModel
from jwtserver.api.v1.help_func.gen_token_secret import secret
from loguru import logger
from base64 import b64decode
from json import loads
from datetime import datetime, timedelta
from jwtserver.schemas import UserPD
from jwtserver.functions.config import load_config

cfg = load_config().token

access_time = timedelta(minutes=cfg.access_expire_time)
refresh_time = timedelta(minutes=cfg.refresh_expire_time)


class AccessTokenEx(Exception):
    def __init__(self, text="Please load access token"):
        self.txt = text


class RefreshTokenEx(Exception):
    def __init__(self, text="Please load refresh token"):
        self.txt = text


class UserEx(Exception):
    def __init__(self, message="Please load user instance"):
        self.message = message
        super().__init__(self.message)


class Data(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class TokenProcessor:
    def __init__(
            self,
            refresh_token: str = None,
            access_token: str = None,
            user: UserPD = None
    ):
        self.user = user
        self.access = access_token
        self.new_access = access_token
        self.refresh = refresh_token
        self.new_refresh = refresh_token

    def payload_token_untested(self, token_type: Literal['access', 'refresh']):
        """Token untested payload
        :param str token_type:
        :return dict data: token payload
        """
        return loads(b64decode(getattr(self, token_type).split('.', 2)[1] + '=='))

    def payload_token(self, token_type: Literal['access', 'refresh']):
        """Token tested payload
        :param str token_type:
        :return dict data: token payload
        :raises JWTError: If the signature is invalid in any way
        :raises ExpiredSignatureError: If the signature has expired
        :raises JWTClaimsError: If any claim is invalid in any way
        """
        return jwt.decode(getattr(self, token_type), cfg.secret_key, algorithms=[cfg.algorithm])

    def create_pair_tokens(self):
        if not self.user:
            raise UserEx
        user_uuid = self.user.uuid.hex if self.user else self.payload_token_untested('access')[
            'uuid']
        datetime_now = datetime.now()
        secret_sol = (datetime_now + access_time).timestamp()
        payload_access = {
            "uuid": user_uuid,
            "secret": secret(user_uuid, sol=secret_sol)[:32],
            "exp": secret_sol
        }

        payload_refresh = {
            "secret": secret(user_uuid, sol=secret_sol)[32:],
            "exp": (datetime_now + refresh_time).timestamp(),
        }

        access_jwt = jwt.encode(payload_access, cfg.secret_key, algorithm=cfg.algorithm)
        refresh_jwt = jwt.encode(payload_refresh, cfg.secret_key, algorithm=cfg.algorithm)
        logger.info(f'{access_jwt}')
        logger.info(f'{refresh_jwt}')
        self.new_access = access_jwt
        self.new_refresh = refresh_jwt
        return access_jwt, refresh_jwt

    # async def response_refresh_token(self, refresh_token: str = Cookie(None)):
    #     # if not refresh_token:
    #     #     raise HTTPException(status_code=400, detail="Invalid refresh token")
    #     return refresh_token
    #
    # def code_validation(self, code, telephone):
    #     value = redis.get(telephone)
    #     code_in_redis = value if value else None
    #     if code != code_in_redis:
    #         raise HTTPException(status_code=400, detail="Fake user")
    #     return code
