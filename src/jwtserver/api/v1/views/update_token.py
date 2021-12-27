from typing import Optional
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from jwtserver.api.v1.help_func.gen_token_secret import secret
from jwtserver.functions.config import load_config
from jwtserver.models import User
from jwtserver.app import app
from fastapi import Depends, Cookie, HTTPException, Response, Header

from jwtserver.api.v1.help_func.ParseToken import TokenProcessor
from jwtserver.functions.session_db import async_db_session

config_token = load_config().token


class Data(BaseModel):
    access_token: str

    class Config:
        orm_mode = True


async def get_current_active_user(Authorization: str = Header(...),
                                  session: AsyncSession = Depends(async_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User is inactive",
        headers={"WWW-Authenticate": "JSv1"},
    )
    token = TokenProcessor(access_token=Authorization.split()[1])
    user = await session.get(User, token.payload_token_untested('access')['uuid'])
    if not user.is_active:
        raise credentials_exception
    return user


# @app.post("/api/v1/auth/reg_user", response_model=schemas.TokenPD)
@app.get("/api/v1/auth/update_token/")
async def refresh_new_access_token(
        response: Response,
        Authorization: str = Header(...),
        refresh_token: Optional[str] = Cookie(None),
        current_user: User = Depends(get_current_active_user),
):
    token = TokenProcessor(access_token=Authorization.split()[1], refresh_token=refresh_token)
    payload_access_untested = token.payload_token_untested('access')
    payload_refresh_token = token.payload_token('refresh')

    try:
        _secret_full = payload_access_untested['secret'] + payload_refresh_token['secret']

        if not _secret_full:
            return {"error": "invalid pair of tokens"}

        if _secret_full == secret(payload_access_untested['uuid'], payload_access_untested['exp']):
            access_token, refresh_token = token.create_pair_tokens(current_user.uuid.hex)

            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                max_age=config_token.refresh_expire_time * 60)

            return {"access_token": access_token, "token_type": "JSv1"}
    except AttributeError:
        return {"error": "token won't find"}
