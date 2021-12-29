from typing import Literal

from fastapi import HTTPException
from fastapi.param_functions import Optional, Cookie
from jose import JWTError, jwt
from pydantic import BaseModel
from starlette import status

from jwtserver.api.v1.help_func.gen_token_secret import secret
from loguru import logger
from base64 import b64decode
from json import loads
from datetime import datetime, timedelta
from jwtserver.functions.config import load_config

cfg = load_config().token

access_time = timedelta(minutes=cfg.access_expire_time)
refresh_time = timedelta(minutes=cfg.refresh_expire_time)


class Data(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class TokenProcessor:
    def __init__(
            self,
            refresh_token: str = None,
            access_token: str = None,
    ):
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
        try:
            return jwt.decode(getattr(self, token_type), cfg.secret_key,
                              algorithms=[cfg.algorithm])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad JWT token",
                headers={"WWW-Authenticate": "JSv1"},
            )

    @staticmethod
    def create_pair_tokens(uuid):
        """Create two JWT tokens with a shared secret at the same time
        :return tuple: [access_token, refresh_token]
        """
        datetime_now = datetime.now()
        secret_sol = (datetime_now + access_time).timestamp()
        payload_access = {
            "uuid": uuid,
            "secret": secret(uuid, sol=secret_sol)[:32],
            "exp": secret_sol
        }

        payload_refresh = {
            "secret": secret(uuid, sol=secret_sol)[32:],
            "exp": (datetime_now + refresh_time).timestamp(),
        }

        access_jwt = jwt.encode(payload_access, cfg.secret_key, algorithm=cfg.algorithm)
        refresh_jwt = jwt.encode(payload_refresh, cfg.secret_key, algorithm=cfg.algorithm)
        logger.info(f'create new {access_jwt=}')
        logger.info(f'create mew {refresh_jwt=}')
        return access_jwt, refresh_jwt
