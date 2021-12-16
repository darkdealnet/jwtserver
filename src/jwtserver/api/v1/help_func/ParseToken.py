from fastapi.param_functions import Optional, Cookie
from jose import JWTError, jwt
from pydantic import BaseModel
from jwtserver.api.v1.help_func.gen_token_secret import secret
from jwtserver.functions.init_redis import redis
from fastapi import HTTPException
from loguru import logger
from base64 import b64decode
from json import loads
from datetime import datetime, timedelta
from jwtserver.schemas import UserPD
from jwtserver.functions.config import load_config

config = load_config().token

access_time = timedelta(minutes=config.access_expire_time)
refresh_time = timedelta(minutes=config.refresh_expire_time)


class AccessTokenNone(Exception):
    def __init__(self, text="Please load access token"):
        self.txt = text


class RefreshTokenNone(Exception):
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

    def payload_access_token_untested(self, access=None):
        _access = access if access else self.access
        if _access:
            return loads(b64decode(_access.split('.', 2)[1] + '=='))
        raise AccessTokenNone

    def payload_refresh_token_untested(self, refresh=None):
        _refresh = refresh if refresh else self.refresh
        if _refresh:
            return loads(b64decode(_refresh.split('.', 2)[1] + '=='))
        raise RefreshTokenNone

    def payload_refresh_token(self, refresh=None):
        _refresh = refresh if refresh else self.refresh
        try:
            return jwt.decode(_refresh, config.secret_key, algorithms=[config.algorithm])
        except JWTError as error:
            logger.critical(error)
        return None

    def payload_access_token(self, access=None):
        _access = access if access else self.access
        try:
            return jwt.decode(_access, config.secret_key, algorithms=[config.algorithm])
        except JWTError as error:
            logger.critical(error)
        return None

    def create_pair_tokens(self):
        if not self.user:
            raise UserEx
        user_uuid = self.user.uuid.hex if self.user else self.payload_access_token_untested()['uuid']
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

        if self.user.is_admin:
            payload_access.update({"isAdmin": self.user.is_admin})

        access_jwt = jwt.encode(payload_access, config.secret_key, algorithm=config.algorithm)
        refresh_jwt = jwt.encode(payload_refresh, config.secret_key, algorithm=config.algorithm)
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
